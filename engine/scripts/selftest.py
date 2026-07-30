#!/usr/bin/env python3
"""End-to-end check of the grader against the exercise pack.

build_db.py verifies the pack using its own compile-and-run logic. This script
verifies the thing students actually hit -- engine.evaluator -- by submitting,
for every exercise:

  * the reference solution, which MUST be graded as a pass, and
  * a do-nothing stub, which MUST be graded as a failure.

Run it after touching the evaluator, the compiler, or the pack.

Usage:
    python3 engine/scripts/selftest.py
    python3 engine/scripts/selftest.py --only ft_split -v
"""

import argparse
import json
import os
import shutil
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.evaluator import Evaluator
from engine.exercises import load_all, spec
from engine.state import DB_FILE


def materialise(rendu, exercise, sources):
    directory = os.path.join(rendu, exercise["name"])
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory)
    for filename, text in sources.items():
        with open(os.path.join(directory, filename), "w", encoding="utf-8") as f:
            f.write(text.strip("\n") + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="test a single exercise by name")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # The graded exercise dicts come from the built database, so this also
    # catches a database that has drifted from the pack. Read straight off disk
    # rather than through StateManager, which would migrate the real progress
    # file of whoever is running the tests.
    with open(DB_FILE, encoding="utf-8") as f:
        graded = dict(json.load(f).get("exercises", {}))

    pack = load_all()
    if args.only:
        pack = [e for e in pack if e["name"] == args.only]
        if not pack:
            print(f"no exercise named {args.only!r}", file=sys.stderr)
            return 1

    missing = [e["name"] for e in pack if e["name"] not in graded]
    if missing:
        print(
            "These exercises are in the pack but not in the database. "
            "Run build_db.py.\n  " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    failures = []
    with tempfile.TemporaryDirectory() as rendu:
        evaluator = Evaluator(rendu)

        for exercise in pack:
            name = exercise["name"]
            entry = graded[name]

            materialise(rendu, exercise, spec.reference_sources(exercise))
            result = evaluator.evaluate(entry)
            if not result.get("ok"):
                failures.append(
                    f"{name}: the REFERENCE solution was rejected "
                    f"({result['stage']}: {result['message']})"
                )
                print(f"  FAIL  {name:<22} reference rejected", file=sys.stderr)
                continue

            stub_sources = dict(spec.reference_sources(exercise))
            stub_sources[exercise["files"][0]] = spec.make_stub(exercise)
            materialise(rendu, exercise, stub_sources)
            stub_result = evaluator.evaluate(entry)
            if stub_result.get("ok"):
                failures.append(
                    f"{name}: a do-nothing STUB was accepted -- this exercise "
                    "asserts nothing"
                )
                print(f"  FAIL  {name:<22} stub accepted", file=sys.stderr)
                continue

            if args.verbose:
                print(
                    f"  ok    {name:<22} reference passes "
                    f"({result['total']} tests), stub fails "
                    f"({stub_result['stage']})"
                )
            else:
                print(f"  ok    {name}")

    if failures:
        print(f"\n{len(failures)} failure(s):\n", file=sys.stderr)
        for message in failures:
            print(f"* {message}", file=sys.stderr)
        return 1

    print(f"\n{len(pack)} exercises: every reference passes, every stub fails.")

    ui_failures = check_ui()
    if ui_failures:
        print(f"\n{len(ui_failures)} UI failure(s):\n", file=sys.stderr)
        for message in ui_failures:
            print(f"* {message}", file=sys.stderr)
        return 1
    return 0


def check_ui():
    """Drive every command, including failure paths, in every language.

    `lang thai` used to raise TypeError because no test ever reached the
    unknown-language branch. Anything reachable from the prompt gets exercised
    here, so a crash in a rarely-taken path shows up as a test failure.
    """
    from engine.i18n import LANGUAGES, validate_catalog
    from engine.main import Shell

    problems = list(validate_catalog())

    invocations = [
        ("status", None), ("subject", None), ("hint", None), ("list", None),
        ("help", None), ("history", None), ("archive", None), ("skip", None),
        ("grademe", None), ("exam", None), ("version", None),
        # Failure and edge paths, which are the ones that go untested.
        ("lang", ""), ("lang", "th"), ("lang", "thai"), ("lang", "en"),
        ("lang", "english"), ("lang", "xyz"), ("lang", "  "), ("lang", "TH"),
        ("exam", "02"), ("exam", "exam_02"), ("exam", "exam 02"), ("exam", "2"),
        ("exam", "extra"), ("exam", "EXTRA"), ("exam", "9"), ("exam", "nope"),
        ("exam", ""), ("exam", "  "),
        ("list", "all"), ("list", "extra"), ("list", "01"), ("list", "nope"),
    ]

    saved_env = {k: os.environ.get(k) for k in
                 ("EXAMSHELP_STATE", "EXAMSHELP_RENDU", "EXAMSHELP_SUBJECTS",
                  "EXAMSHELP_HISTORY", "EXAMSHELP_NO_UPDATE_CHECK")}
    with tempfile.TemporaryDirectory() as tmp:
        # A test run must not depend on the network, so `version` and the
        # background check both take their no-op path here.
        os.environ["EXAMSHELP_NO_UPDATE_CHECK"] = "1"
        # Redirect the whole workspace before Shell() builds any state, so the
        # real .examshelp_state.json and rendu/ are never touched.
        os.environ["EXAMSHELP_STATE"] = os.path.join(tmp, "state.json")
        os.environ["EXAMSHELP_RENDU"] = os.path.join(tmp, "rendu")
        os.environ["EXAMSHELP_SUBJECTS"] = os.path.join(tmp, "subjects")
        os.environ["EXAMSHELP_HISTORY"] = os.path.join(tmp, "history")
        for lang in LANGUAGES:
            shell = Shell()
            shell.state.set_language(lang)
            shell.ui.lang = lang
            shell.evaluator.lang = lang

            for name, argument in invocations:
                try:
                    shell.ui.clear_buffer()
                    if not shell.dispatch(name, argument):
                        problems.append(f"[{lang}] `{name}` did not dispatch")
                        continue
                    shell.ui.prompt(shell.state.get_session_name())
                except Exception as err:
                    problems.append(
                        f"[{lang}] `{name} {argument or ''}`.strip() raised "
                        f"{type(err).__name__}: {err}"
                    )

            try:
                shell.ui.clear_buffer()
                if shell.dispatch("definitely_not_a_command"):
                    problems.append(f"[{lang}] unknown command was dispatched")
            except Exception as err:
                problems.append(f"[{lang}] unknown command raised {type(err).__name__}: {err}")

    for key, value in saved_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    if not problems:
        print(f"UI: every command ran in {len(LANGUAGES)} languages, catalogs consistent.")
    return problems


if __name__ == "__main__":
    sys.exit(main())
