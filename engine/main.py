#!/usr/bin/env python3
"""ExamsHelp -- a practice harness for the 42 exams.

Run `./examshelp` for the interactive shell, or `./examshelp <command>` for a
single command.
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine import update
from engine.evaluator import Evaluator
from engine.i18n import LANGUAGES, accepted_languages, t, track_name
from engine.state import StateManager
from engine.tracks import accepted_tracks, resolve_track
from engine.ui.ansi import DIM, RESET, YELLOW
from engine.ui.terminal import TerminalUI
from engine.version import VERSION

COMMANDS = (
    "status", "subject", "hint", "grademe", "skip", "list", "exam", "examselect",
    "lang", "archive", "history", "reset", "version", "help", "exit",
)


class Shell:
    def __init__(self):
        self.state = StateManager()
        lang = self.state.get_language()
        self.ui = TerminalUI(lang=lang)
        self.evaluator = Evaluator(self.state.workspace_rendu, lang=lang)
        # What we heard last time; this start refreshes it for the next one.
        self.newer_version = update.pending(self.state.state_file)
        update.refresh_later(self.state.state_file)

    def tr(self, key, **kwargs):
        return t(self.ui.lang, key, **kwargs)

    # ------------------------------------------------------------- commands

    def cmd_status(self, _args=None):
        self.ui.display_status(self.state.get_progress_data())

    def cmd_subject(self, _args=None):
        self.ui.display_subject(
            self.state.get_current_exercise(), self.state.get_current_track()
        )

    def cmd_hint(self, _args=None):
        self.ui.display_hints(self.state.get_current_exercise())

    def cmd_grademe(self, _args=None):
        exercise = self.state.get_current_exercise()
        if not exercise:
            self.ui.err(self.tr("shell.no_exercise"))
            return
        files = exercise["expected_files"]
        if isinstance(files, str):
            files = [f.strip() for f in files.split(",")]
        self.ui.info(
            self.tr("grade.running", name=exercise["name"], files=", ".join(files))
        )
        result = self.evaluator.evaluate(exercise)
        self.ui.display_eval_result(result, exercise)
        if result.get("ok"):
            self.state.complete_current_exercise()
            following = self.state.get_current_exercise()
            if following:
                self.ui.ok("  " + self.tr("grade.next_up", name=following["name"]))

    def cmd_skip(self, _args=None):
        old_name, new_exercise = self.state.skip_current_exercise()
        track = self.state.get_current_track()
        self.ui.display_skip(old_name, new_exercise, track)
        # Skipping is how you go looking for a different problem, so show it
        # rather than making the reader type `subject` every single time.
        if new_exercise:
            self.ui.display_subject(new_exercise, track)

    def cmd_list(self, args=None):
        target = (args or "").strip()
        if target.lower() in ("all", "*"):
            tracks = self.state.available_tracks()
        elif target:
            track = self._resolve_track(target)
            if not track:
                return
            tracks = [track]
        else:
            tracks = [self.state.get_current_track()]
        self.ui.display_exercise_list(self.state, tracks)

    def cmd_exam(self, args=None):
        target = (args or "").strip()
        if not target:
            self.ui.display_exams(self.state.track_summary())
            self.ui.dim(
                "  "
                + self.tr(
                    "exam.current",
                    track=track_name(self.ui.lang, self.state.get_current_track()),
                )
            )
            return

        track = self.state.set_current_track(target)
        if not track:
            self.ui.err(
                self.tr("exam.unknown", name=target, accepted=accepted_tracks())
            )
            return
        self.ui.ok(
            "  "
            + self.tr(
                "exam.set",
                track=track_name(self.ui.lang, track),
                level=self.state.get_level(track),
            )
        )
        self.cmd_subject()

    def cmd_examselect(self, args=None):
        target = (args or "").strip()
        if not target:
            self.ui.display_exercise_list(self.state, self.state.available_tracks())
            self.ui.dim("  " + self.tr("select.hint"))
            return

        name, candidates, kind = self.state.match_exercise(target)
        if not name:
            if not candidates:
                self.ui.err(self.tr("select.unknown", name=target))
            else:
                key = "select.ambiguous" if kind == "ambiguous" else "select.did_you_mean"
                self.ui.err(
                    self.tr(key, name=target, suggestions=", ".join(candidates))
                )
            return

        exercise = self.state.jump_to_exercise(name)
        track = self.state.get_current_track()
        self.ui.ok(
            "  "
            + self.tr(
                "select.jumped",
                name=exercise["name"],
                track=track_name(self.ui.lang, track),
                level=self.state.get_level(track),
            )
        )
        self.cmd_subject()

    def _resolve_track(self, target):
        """Resolve a track argument, reporting the failure to the user."""
        track = resolve_track(target)
        if track not in self.state.available_tracks():
            self.ui.err(
                self.tr("exam.unknown", name=target, accepted=accepted_tracks())
            )
            return None
        return track

    def cmd_lang(self, args=None):
        target = (args or "").strip().lower()
        if not target:
            self.ui.info(self.tr("shell.lang_current", lang=self.ui.lang))
            return
        code = self.state.set_language(target)
        if not code:
            self.ui.err(
                self.tr("shell.lang_unknown", lang=target,
                        accepted=accepted_languages())
            )
            return

        self.ui.lang = code
        self.evaluator.lang = code
        entry = LANGUAGES[code]
        self.ui.ok(
            "  " + self.tr("shell.lang_set", flag=entry["flag"], name=entry["name"])
        )
        self.cmd_subject()

    def cmd_archive(self, _args=None):
        folder, meta = self.state.archive_current_session(clean_workspace=False)
        self.ui.display_archive(meta["session_name"], folder, cleaned=False)

    def cmd_history(self, _args=None):
        self.ui.display_sessions_history(self.state.session_mgr.list_saved_sessions())

    def cmd_reset(self, _args=None):
        if not self._confirm(self.tr("shell.confirm_reset")):
            self.ui.dim("  " + self.tr("shell.cancelled"))
            return
        self.state.reset_all_progress()
        self.ui.display_reset(
            self.state.get_current_exercise(), self.state.get_current_track()
        )

    def cmd_version(self, _args=None):
        """Typed by hand, so this one is allowed to wait on the network."""
        latest = update.check_now(self.state.state_file)
        if latest is None:
            self.ui.dim("  " + self.tr("update.unknown", current=VERSION))
        elif update.is_newer(latest):
            self.newer_version = latest
            self.ui.warn("  " + self.tr("update.available", latest=latest, current=VERSION))
            self.ui.dim("  " + self.tr("update.how"))
        else:
            self.ui.ok("  " + self.tr("update.current", current=VERSION))

    def cmd_help(self, _args=None):
        self.ui.display_help()

    def _confirm(self, question):
        """Ask outside the buffered view -- the answer has to be live."""
        try:
            answer = input(f"{YELLOW}{question}{RESET} [y/N] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return False
        return answer in ("y", "yes")

    # ---------------------------------------------------------------- loops

    def dispatch(self, name, args=None):
        handler = getattr(self, f"cmd_{name}", None)
        if handler is None:
            return False
        handler(args)
        return True

    def run_interactive(self):
        self.ui.print_banner(
            self.state.db.get("total_exercises"),
            self.state.db.get("total_tests"),
            newer_version=self.newer_version,
        )
        self.ui.emit()
        self.cmd_status()
        self.ui.dim("  " + self.tr("shell.help_hint"))
        self.ui.flush()

        while True:
            try:
                raw = input(self.ui.prompt(self.state.get_session_name())).strip()
            except (KeyboardInterrupt, EOFError):
                print()
                self._quit()
                return

            if not raw:
                continue

            name, _, args = raw.partition(" ")
            name = name.lower()

            if name in ("exit", "quit", "q"):
                self._quit()
                return

            if not self.dispatch(name, args):
                self.ui.err(self.tr("shell.unknown_command", name=name))
            self.ui.flush()

    def _quit(self):
        folder, meta = self.state.archive_current_session(clean_workspace=False)
        self.ui.display_archive(meta["session_name"], folder, cleaned=False)
        self.ui.info(self.tr("shell.goodbye"))
        self.ui.flush()


def main():
    parser = argparse.ArgumentParser(
        description="ExamsHelp -- practice harness for the 42 exams."
    )
    parser.add_argument(
        "command", nargs="?", choices=COMMANDS, help="run one command and exit"
    )
    parser.add_argument("argument", nargs="?", help="argument for that command")
    args = parser.parse_args()

    shell = Shell()

    if not shell.state.has_exercises():
        print(shell.tr("shell.no_db"), file=sys.stderr)
        print(f"{DIM}  {shell.tr('shell.build_db')}{RESET}", file=sys.stderr)
        return 1

    if args.command in ("exit", "quit"):
        return 0

    if args.command:
        shell.dispatch(args.command, args.argument)
        shell.ui.flush()
        return 0

    shell.run_interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
