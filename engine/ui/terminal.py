"""Everything the user sees.

Output is collected into self.lines and then flushed with print(), so the shell
scrolls like a normal shell. An earlier version drew a fixed full-screen layout
that redrew in place; it read as claustrophobic in practice, so output simply
appends now. The buffer is kept because one-shot mode and the selftest both want
to render a command without printing it.
"""

import os
import shlex

# Importing readline gives input() arrow-key history and line editing. It also
# decides whether the prompt may use \001/\002 width markers: without readline
# those bytes would be printed literally.
try:
    import readline  # noqa: F401

    HAVE_READLINE = True
except ImportError:
    HAVE_READLINE = False

from engine.hints import HintEngine
from engine.i18n import language_badge, other_language, t, track_name
from engine.tracks import ADDED, EXTRA
from engine.version import VERSION
from engine.ui.ansi import (
    CYAN,
    DIM,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    WHITE,
    YELLOW,
    box_width,
    display_width,
    draw_box,
    visible,
)

MAX_SHOWN_FAILURES = 3
MAX_SHOWN_LINES = 8


class TerminalUI:
    def __init__(self, lang="en"):
        self.lang = lang
        self.lines = []

    # ------------------------------------------------------------ primitives

    def tr(self, key, **kwargs):
        return t(self.lang, key, **kwargs)

    def clear_buffer(self):
        self.lines = []

    def flush(self):
        """Print everything buffered so far and empty the buffer."""
        for line in self.lines:
            print(line)
        self.lines = []

    def emit(self, line=""):
        self.lines.append(line)

    def plain(self, text=""):
        self.emit(text)

    def info(self, text):
        self.emit(f"{CYAN}{text}{RESET}")

    def ok(self, text):
        self.emit(f"{GREEN}{text}{RESET}")

    def warn(self, text):
        self.emit(f"{YELLOW}{text}{RESET}")

    def err(self, text):
        self.emit(f"{RED}{text}{RESET}")

    def dim(self, text):
        self.emit(f"{DIM}{text}{RESET}")

    def box(self, title, lines, color=CYAN, footer=None, indent="  "):
        draw_box(title, lines, color=color, footer=footer, out=self.emit, indent=indent)

    def _field(self, key, value, width=None, color=WHITE):
        name = self.tr(key)
        width = width or (18 if self.lang == "en" else 16)
        pad_amount = max(1, width - display_width(name))
        return f"{MAGENTA}{name}{' ' * pad_amount}{RESET}{color}{value}{RESET}"

    # ---------------------------------------------------------------- prompt

    def prompt(self, session_name):
        """The input prompt. Carries the language badge, which is why it is here.

        Colour escapes are wrapped in \001/\002 so readline does not count them
        towards the line width; without that, editing a long command line makes
        the cursor drift.
        """
        def invisible(sequence):
            if not HAVE_READLINE:
                return sequence
            return f"\001{sequence}\002"

        return (
            f"\n{language_badge(self.lang)} "
            f"{invisible(YELLOW)}{session_name}{invisible(RESET)} "
            f"{invisible(CYAN)}❯{invisible(RESET)} "
        )

    # ---------------------------------------------------------------- banner

    def print_banner(self, exercise_count=None, test_count=None, newer_version=None):
        art = [
            " ███████╗██╗  ██╗██████╗ ███╗   ███╗███████╗██╗  ██╗███████╗██╗     ██████╗ ",
            " ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██╔════╝██║  ██║██╔════╝██║     ██╔══██╗",
            " █████╗   ╚███╔╝ ██████╔╝██╔████╔██║███████╗███████║█████╗  ██║     ██████╔╝",
            " ██╔══╝   ██╔██╗ ██╔═══╝ ██║╚██╔╝██║╚════██║██╔══██║██╔══╝  ██║     ██╔═══╝ ",
            " ███████╗██╔╝ ██╗██║     ██║ ╚═╝ ██║███████╗██║  ██║███████╗███████╗██║     ",
            " ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ",
        ]
        if box_width() >= 78:
            for i, line in enumerate(art):
                self.emit(f"{MAGENTA if i >= 5 else CYAN}{line}{RESET}")
        else:
            self.emit(f"{CYAN}=== ExamsHelp ==={RESET}")

        subtitle = f"{self.tr('app.tagline')}  ·  {VERSION}"
        if exercise_count:
            subtitle += f"  ·  {exercise_count} / {test_count}"
        self.dim(subtitle.center(box_width()))

        if newer_version:
            notice = self.tr("update.available", latest=newer_version, current=VERSION)
            self.warn(notice.center(box_width()))
            self.dim(self.tr("update.how").center(box_width()))

    # ---------------------------------------------------------------- status

    def display_status(self, progress):
        exercise = progress["current_exercise"]

        lines = [
            self._field(
                "field.exam",
                f"{CYAN}{track_name(self.lang, progress['track'])}{RESET}"
                f"{DIM}  ·  {RESET}{WHITE}"
                f"{self.tr('exam.row_level', level=progress['current_level'], total=progress['total_levels'])}"
                f"{RESET}",
                color="",
            ),
            self._field(
                "field.completed",
                f"{GREEN}{self.tr('progress.session', count=progress['session_completed_count'])}"
                f"{RESET}{DIM}  ·  {RESET}{CYAN}"
                f"{self.tr('progress.overall', done=progress['total_completions'], total=progress['total_count'])}"
                f"{RESET}",
                color="",
            ),
        ]

        if exercise:
            files = _as_list(exercise["expected_files"])
            allowed = _as_list(exercise["allowed_functions"])
            lines += [
                "",
                self._field("field.exercise", exercise["name"]),
                self._field("field.type", self.tr(f"kind.{exercise.get('kind', 'program')}"), color=CYAN),
                self._field("field.files", ", ".join(files), color=YELLOW),
                self._field("field.workspace", f"rendu/{exercise['name']}/", color=YELLOW),
                self._field(
                    "field.allowed",
                    ", ".join(allowed) if allowed else self.tr("hint.none"),
                    color=CYAN,
                ),
            ]
            if exercise.get("prototype"):
                lines.append(self._field("field.prototype", exercise["prototype"], color=YELLOW))

        lines.append("")
        lines.append(self._field("ui.language", language_badge(self.lang), color=CYAN))

        self.box(
            f"{CYAN}{self.tr('ui.dashboard')}{RESET}",
            lines,
            color=CYAN,
            footer=f"{DIM}{VERSION}{RESET}",
        )

    # --------------------------------------------------------------- subject

    def _placement(self, exercise, track):
        """Where this exercise sits, as (track, level).

        An exercise appears in several exams at different levels, so the answer
        only means something relative to the track being read.
        """
        exams = exercise.get("exams") or {}
        if track in exams:
            return track, exams[track]
        if exams:
            return min(exams.items(), key=lambda pair: (pair[1], pair[0]))
        return track or EXTRA, 0

    def display_subject(self, exercise, track=None):
        if not exercise:
            self.warn(self.tr("shell.no_exercise"))
            return

        text = exercise.get("subject_th" if self.lang == "th" else "subject", "")
        where, level = self._placement(exercise, track)
        self.box(
            f"{CYAN}{self.tr('ui.subject')}: {exercise['name']}{RESET}",
            _reflow_subject(text),
            color=MAGENTA,
            footer=f"{DIM}"
            f"{self.tr('subject.footer', track=track_name(self.lang, where), level=level)}"
            f"{RESET}",
            indent="",
        )
        # Nothing outside the 2026 pool may be read as real exam material.
        if exercise.get("source") == EXTRA:
            self.dim(f"  {self.tr('track.extra_note')}")
        elif exercise.get("source") == ADDED:
            self.dim(f"  {self.tr('track.added_note')}")
        self.dim(f"  {self.tr('subject.switch', other=other_language(self.lang))}")

    # ----------------------------------------------------------------- hints

    def display_hints(self, exercise):
        if not exercise:
            self.warn(self.tr("shell.no_exercise"))
            return
        hints = HintEngine.get_exercise_hints(exercise, self.lang)
        self.box(
            f"{CYAN}{self.tr('ui.hints')}: {exercise['name']}{RESET}",
            [f"{YELLOW}{i:>2}.{RESET} {h}" for i, h in enumerate(hints, 1)],
            color=YELLOW,
            footer=f"{DIM}{VERSION}{RESET}",
        )

    # ------------------------------------------------------------ evaluation

    def display_eval_result(self, result, exercise=None):
        stage = result.get("stage", "")
        message = self._result_message(result)

        if result.get("ok"):
            lines = [f"{GREEN}{message}{RESET}", f"{DIM}{self.tr('grade.byte_for_byte')}{RESET}"]
            self._advisory_lines(result, lines)
            self.box(
                f"{GREEN}{self.tr('grade.passed')}{RESET}",
                lines,
                color=GREEN,
                footer=f"{DIM}{VERSION}{RESET}",
            )
            return

        lines = [f"{RED}{message}{RESET}"]

        if stage == "compile" and result.get("compiler_log"):
            lines.append("")
            lines.append(f"{YELLOW}{self.tr('grade.compiler_output')}{RESET}")
            for log_line in result["compiler_log"].splitlines()[:14]:
                lines.append(f"{DIM}{log_line}{RESET}")

        if stage == "tests":
            lines.append("")
            lines.append(
                f"{DIM}{self.tr('grade.ratio', passed=result['passed'], total=result['total'])}{RESET}"
            )
            failures = [r for r in result["results"] if r["status"] != "pass"]
            for record in failures[:MAX_SHOWN_FAILURES]:
                lines.append("")
                lines.extend(self._failure_lines(record, exercise))
            if len(failures) > MAX_SHOWN_FAILURES:
                lines.append("")
                lines.append(
                    f"{DIM}{self.tr('grade.more_failures', count=len(failures) - MAX_SHOWN_FAILURES)}{RESET}"
                )

        self._advisory_lines(result, lines)

        self.box(
            f"{RED}{self.tr('grade.not_yet')} · {stage}{RESET}",
            lines,
            color=RED,
            footer=f"{DIM}{VERSION}{RESET}",
        )

        hints = result.get("hints", [])
        if hints:
            self.box(
                f"{YELLOW}{self.tr('grade.look_at')}{RESET}",
                [f"{CYAN}·{RESET} {h}" for h in hints],
                color=YELLOW,
            )

    def _result_message(self, result):
        """Translate the grader's message when it gave us a key to work with."""
        key = result.get("msg_key")
        if key:
            return self.tr(key, **result.get("msg_args", {}))
        return result.get("message", "")

    def _failure_lines(self, record, exercise):
        name = exercise["name"] if exercise else "a.out"
        command = f"./{name}"
        if record["argv"]:
            command += " " + " ".join(shlex.quote(a) for a in record["argv"])

        lines = [
            f"{YELLOW}{self.tr('grade.test', index=record['index'])}{RESET}"
            f"  {DIM}{command}{RESET}"
        ]
        if record.get("note"):
            lines.append(f"{DIM}  ({record['note']}){RESET}")

        if record["status"] == "timeout":
            lines.append(f"{RED}  {self.tr('grade.timed_out', detail=record['detail'])}{RESET}")
            return lines
        if record["status"] == "crash":
            lines.append(f"{RED}  {self.tr('grade.crashed', detail=record['detail'])}{RESET}")
            if record.get("stderr"):
                lines.append(f"{DIM}  {self.tr('grade.stderr', text=record['stderr'])}{RESET}")
            return lines

        expect = self.tr("grade.expect")
        got = self.tr("grade.got")
        width = max(display_width(expect), display_width(got))
        lines.append(
            f"{GREEN}  {expect}{' ' * (width - display_width(expect))} {RESET}"
            f"{self._show(record['expected'])}"
        )
        lines.append(
            f"{RED}  {got}{' ' * (width - display_width(got))} {RESET}"
            f"{self._show(record['got'])}"
        )
        return lines

    def _advisory_lines(self, result, lines):
        advisory = result.get("advisory")
        if advisory:
            lines.append("")
            lines.append(
                f"{YELLOW}!{RESET} {DIM}"
                f"{self.tr('grade.substitution_note', names=', '.join(advisory))}{RESET}"
            )

    def _show(self, text):
        """Render output for comparison, cat -e style, truncated if huge."""
        if text == "":
            return f"{DIM}{self.tr('grade.nothing')}{RESET}"
        lines = visible(text).split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        if len(lines) == 1:
            return lines[0]
        shown = lines[:MAX_SHOWN_LINES]
        suffix = ""
        if len(lines) > MAX_SHOWN_LINES:
            suffix = f" {DIM}(+{len(lines) - MAX_SHOWN_LINES}){RESET}"
        return " ⏎ ".join(shown) + suffix

    # ------------------------------------------------------------ navigation

    def display_skip(self, old_name, new_exercise, track=None):
        if not new_exercise:
            self.warn(self.tr("nav.nothing_left", name=old_name))
            return
        where, level = self._placement(new_exercise, track)
        self.box(
            f"{YELLOW}{self.tr('nav.skipped_title')}{RESET}",
            [
                f"{YELLOW}{self.tr('nav.skipped', name=old_name)}{RESET}",
                f"{GREEN}{self.tr('nav.now_on')}{RESET} {WHITE}{new_exercise['name']}{RESET}"
                f"{DIM}  "
                f"{self.tr('nav.level_note', track=track_name(self.lang, where), level=level)}"
                f"{RESET}",
                f"{DIM}{self.tr('nav.subjects_updated')}{RESET}",
            ],
            color=YELLOW,
        )

    def display_reset(self, new_exercise, track=None):
        where, _ = self._placement(new_exercise or {}, track)
        lines = [
            f"{GREEN}{self.tr('nav.reset_done', track=track_name(self.lang, where))}{RESET}"
        ]
        if new_exercise:
            lines.append(
                f"{DIM}{self.tr('nav.starting_from')}{RESET} {WHITE}{new_exercise['name']}{RESET}"
            )
        self.box(f"{RED}{self.tr('nav.reset_title')}{RESET}", lines, color=RED)

    def display_archive(self, session_name, folder, cleaned):
        if folder is None:
            self.dim(f"  {self.tr('nav.nothing_to_archive')}")
            return
        lines = [
            f"{CYAN}{self.tr('nav.archived')}{RESET} {YELLOW}{session_name}{RESET}",
            f"{DIM}{self.tr('nav.archived_to')}{RESET} {GREEN}{os.path.relpath(folder)}{RESET}",
            f"{DIM}{self.tr('nav.rendu_cleared' if cleaned else 'nav.rendu_kept')}{RESET}",
        ]
        self.box(f"{YELLOW}{self.tr('nav.session_saved')}{RESET}", lines, color=YELLOW)

    def display_sessions_history(self, sessions):
        if not sessions:
            self.warn(self.tr("nav.no_sessions"))
            return
        header = (
            f"{MAGENTA}{self.tr('list.col_session'):<28}"
            f"{self.tr('list.col_archived'):<21}"
            f"{self.tr('list.col_level'):<7}"
            f"{self.tr('list.col_done')}{RESET}"
        )
        lines = [header]
        for s in sessions:
            lines.append(
                f"{YELLOW}{s['session_name']:<28}{RESET}"
                f"{DIM}{s.get('archived_at', '?'):<21}{RESET}"
                f"{s.get('current_level', 0):<7}"
                f"{GREEN}{s.get('completed_count', 0)}{RESET}"
            )
        self.box(f"{CYAN}{self.tr('ui.history')}{RESET}", lines, color=CYAN)

    def display_exercise_list(self, state, tracks):
        """The ladder for each requested track, level by level."""
        completed = set(state.state.get("completed_exercises", []))
        current_track = state.get_current_track()

        lines = []
        for track in tracks:
            levels = state.track_levels(track)
            current_level = state.get_level(track)
            active = state.get_active_name(track)

            if lines:
                lines.append("")
            heading = f"{MAGENTA}{track_name(self.lang, track)}{RESET}"
            if track == current_track:
                heading = f"{YELLOW}▸{RESET} {heading}"
            if track == EXTRA:
                heading += f"  {DIM}{self.tr('track.extra_note')}{RESET}"
            lines.append(heading)

            for level_key in sorted(levels, key=int):
                exercises = state.exercises_at(track, level_key)
                if not exercises:
                    continue
                level = int(level_key)
                done = sum(1 for e in exercises if e["name"] in completed)
                locked = track == current_track and level > current_level
                head = DIM if locked else CYAN
                lines.append(
                    f"{head}{self.tr('list.level', level=level)}{RESET} {DIM}"
                    f"{self.tr('list.progress', done=done, total=len(exercises), locked=self.tr('list.locked_suffix') if locked else '')}"
                    f"{RESET}"
                )
                for exercise in sorted(exercises, key=lambda e: e["name"]):
                    name = exercise["name"]
                    if name in completed:
                        mark, color = "✓", GREEN
                    elif name == active and track == current_track:
                        mark, color = "▸", YELLOW
                    elif locked:
                        mark, color = "·", DIM
                    else:
                        mark, color = " ", RESET
                    kind = "fn" if exercise.get("kind") == "function" else "prog"
                    count = len(exercise.get("tests", []))
                    key = "list.tests" if count == 1 else "list.tests_plural"
                    label = name + ("*" if exercise.get("source") == ADDED else "")
                    lines.append(
                        f"{color}{mark} {label:<22}{RESET}"
                        f"{DIM}{kind:<5}{self.tr(key, count=count)}{RESET}"
                    )

        legend = (
            f"{GREEN}✓{RESET} {self.tr('list.legend_done')}   "
            f"{YELLOW}▸{RESET} {self.tr('list.legend_current')}   "
            f"{DIM}·{RESET} {self.tr('list.legend_locked')}   "
            f"{DIM}*{RESET} {self.tr('list.legend_added')}"
        )
        self.box(
            f"{CYAN}{self.tr('ui.curriculum')}{RESET}",
            lines,
            color=CYAN,
            footer=None,
        )
        self.dim("  " + legend)
        self.dim("  " + self.tr("list.all_hint"))

    def display_exams(self, rows):
        """Every track with its progress, for the `exam` command."""
        labels = {row["track"]: track_name(self.lang, row["track"]) for row in rows}
        width = max((display_width(label) for label in labels.values()), default=0)

        lines = []
        for row in rows:
            mark, color = ("▸", YELLOW) if row["current"] else (" ", RESET)
            label = labels[row["track"]]
            padding = " " * max(1, width - display_width(label) + 2)
            line = (
                f"{color}{mark} {label}{RESET}{padding}"
                f"{DIM}{self.tr('exam.row_level', level=row['level'], total=row['total_levels'])}"
                f"{RESET}   {GREEN}"
                f"{self.tr('exam.row_done', done=row['done'], total=row['total'])}{RESET}"
            )
            lines.append(line)

        self.box(f"{CYAN}{self.tr('ui.exams')}{RESET}", lines, color=CYAN)
        # Below the box, not in the row: appended inline it overflows the box
        # width and the wrapper collapses the column alignment.
        if any(row["track"] == EXTRA for row in rows):
            self.dim(f"  {track_name(self.lang, EXTRA)} — {self.tr('track.extra_note')}")

    def display_help(self):
        names = [
            "subject", "hint", "grademe", "status", "list", "exam",
            "skip", "lang", "archive", "history", "reset", "version", "exit",
        ]
        width = 12
        lines = [
            f"{GREEN}{name:<{width}}{RESET}{DIM}{self.tr(f'cmd.{name}')}{RESET}"
            for name in names
        ]
        self.box(
            f"{CYAN}{self.tr('ui.commands')}{RESET}",
            lines,
            color=CYAN,
            footer=f"{DIM}{VERSION}{RESET}",
        )


def _reflow_subject(text):
    """Join prose into paragraphs so it re-wraps to the current terminal width.

    Indented lines, shell transcripts and the metadata header are kept verbatim:
    their line structure is part of the meaning.
    """
    lines = []
    paragraph = []

    def flush():
        if paragraph:
            lines.append(f"{WHITE}{' '.join(paragraph)}{RESET}")
            paragraph.clear()

    for raw in text.splitlines():
        verbatim = (
            not raw.strip()
            or raw[:1].isspace()
            or raw.lstrip().startswith("$>")
            or " : " in raw
        )
        if verbatim:
            flush()
            lines.append(f"{WHITE}{raw}{RESET}" if raw.strip() else "")
        else:
            paragraph.append(raw.strip())
    flush()
    return lines


def _as_list(value):
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return list(value or [])
