#!/usr/bin/env python3
"""Generate engine/config/exercises_db.json from the exercise pack.

For every exercise this script:

  1. compiles the reference solution with -Wall -Wextra -Werror,
  2. runs it against each declared input and records what it printed,
  3. compiles a do-nothing stub and requires it to FAIL at least one test.

Step 3 is the important one. The database this replaced was written by hand, and
105 of its 118 exercises expected `null` output from every test -- so an empty
`int main(void){return 0;}` scored "All 3/3 tests passed". An exercise that
cannot tell a real solution from a stub is a broken exercise, and this build
refuses to ship one.

Usage:
    python3 engine/scripts/build_db.py             # build, refuse on any failure
    python3 engine/scripts/build_db.py --check     # verify without writing
    python3 engine/scripts/build_db.py --only NAME # work on a single exercise
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.exercises import load_all, spec
from engine.tracks import EXTRA, PISCINE_2026, TRACKS

DB_PATH = os.path.join(BASE_DIR, "engine", "config", "exercises_db.json")
CFLAGS = ["-Wall", "-Wextra", "-Werror"]
RUN_TIMEOUT = 5


class BuildError(Exception):
    pass


def compile_solution(work_dir, exercise, sources, tag):
    """Compile a {filename: text} map plus the harness. Returns the binary path."""
    src_dir = os.path.join(work_dir, tag)
    os.makedirs(src_dir, exist_ok=True)

    c_files = []
    for filename, text in sources.items():
        path = os.path.join(src_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.strip("\n") + "\n")
        if filename.endswith(".c"):
            c_files.append(path)

    if exercise["harness"]:
        harness_path = os.path.join(src_dir, "__harness.c")
        with open(harness_path, "w", encoding="utf-8") as f:
            f.write(exercise["harness"].strip("\n") + "\n")
        c_files.append(harness_path)

    binary = os.path.join(src_dir, "a.out")
    result = subprocess.run(
        ["gcc"] + CFLAGS + ["-I", src_dir, "-o", binary] + c_files,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise BuildError(
            f"{exercise['name']}: {tag} does not compile\n{result.stderr.strip()}"
        )
    return binary


def run_test(binary, test):
    proc = subprocess.run(
        [binary] + test["argv"],
        input=test["stdin"],
        capture_output=True,
        text=True,
        timeout=RUN_TIMEOUT,
    )
    return proc.stdout, proc.returncode


def build_exercise(exercise):
    """Run the reference against every input and return the expected results."""
    with tempfile.TemporaryDirectory() as work_dir:
        reference = compile_solution(
            work_dir, exercise, spec.reference_sources(exercise), "reference"
        )

        expected = []
        for test in exercise["tests"]:
            try:
                stdout, returncode = run_test(reference, test)
            except subprocess.TimeoutExpired:
                raise BuildError(
                    f"{exercise['name']}: reference solution timed out on "
                    f"argv={test['argv']}"
                )
            if returncode != 0:
                raise BuildError(
                    f"{exercise['name']}: reference solution exited with "
                    f"{returncode} on argv={test['argv']}"
                )
            # A second run must agree, or the test is not deterministic and would
            # fail students at random.
            again, _ = run_test(reference, test)
            if again != stdout:
                raise BuildError(
                    f"{exercise['name']}: reference output is not deterministic "
                    f"for argv={test['argv']}"
                )
            expected.append(
                {
                    "argv": test["argv"],
                    "stdin": test["stdin"],
                    "note": test["note"],
                    "expected_stdout": stdout,
                }
            )

        _assert_stub_fails(work_dir, exercise, expected)
        _verify_subject_examples(reference, exercise)

    return expected


def _parse_transcripts(subject):
    """Pull `$> ./prog args | cat -e` transcripts and their output out of a subject.

    Yields (argv, expected_lines) so the build can prove that every example a
    student reads is what the reference actually prints.
    """
    lines = subject.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped.startswith("$>"):
            i += 1
            continue

        command = stripped[2:].strip()
        if command.endswith("| cat -e"):
            command = command[: -len("| cat -e")].strip()
        try:
            argv = shlex.split(command)
        except ValueError:
            i += 1
            continue
        if not argv or not argv[0].startswith("./"):
            i += 1
            continue

        # Expected-output lines are indented to match the `$>` line. Strip exactly
        # that prefix rather than lstrip()-ing, because leading spaces can be part
        # of the expected output (str_capitalizer preserves them).
        indent = " " * (len(raw) - len(raw.lstrip()))

        i += 1
        output = []
        while i < len(lines):
            candidate = lines[i]
            if candidate.startswith(indent):
                candidate = candidate[len(indent):]
            else:
                candidate = candidate.lstrip()
            if candidate.strip().startswith("$>") or not candidate.endswith("$"):
                break
            output.append(candidate[:-1])
            i += 1
        yield argv[1:], output


def _verify_subject_examples(binary, exercise):
    """Prove that every shell transcript in the subject is real.

    Prose examples ("ft_range(1, 3) -> [1, 2, 3]") are not transcripts and are
    skipped; anything written as a `$> ./prog ...` session is executed.
    """
    for argv, want_lines in _parse_transcripts(exercise["subject"]):
        stdout, _ = run_test(binary, {"argv": argv, "stdin": ""})
        got_lines = stdout.split("\n")
        if got_lines and got_lines[-1] == "":
            got_lines.pop()
        if got_lines != want_lines:
            raise BuildError(
                f"{exercise['name']}: the subject shows an example that the "
                f"reference solution does not produce.\n"
                f"    argv:     {argv}\n"
                f"    subject:  {want_lines}\n"
                f"    actual:   {got_lines}"
            )


def _assert_stub_fails(work_dir, exercise, expected):
    """The honesty check: a do-nothing solution must not pass these tests."""
    stub_sources = dict(spec.reference_sources(exercise))
    stub_sources[exercise["files"][0]] = spec.make_stub(exercise)

    try:
        stub = compile_solution(work_dir, exercise, stub_sources, "stub")
    except (BuildError, subprocess.TimeoutExpired):
        # A stub that will not even compile certainly cannot pass.
        return

    for test, want in zip(exercise["tests"], expected):
        try:
            stdout, returncode = run_test(stub, test)
        except subprocess.TimeoutExpired:
            return
        if returncode != 0 or stdout != want["expected_stdout"]:
            return

    raise BuildError(
        f"{exercise['name']}: a do-nothing stub passes every test, so this "
        "exercise asserts nothing. Add inputs that produce distinguishable output."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify every exercise without writing the database",
    )
    parser.add_argument("--only", help="build just one exercise, by name")
    args = parser.parse_args()

    exercises = load_all()
    if args.only:
        exercises = [e for e in exercises if e["name"] == args.only]
        if not exercises:
            print(f"no exercise named {args.only!r}", file=sys.stderr)
            return 1

    entries = {}
    failures = []
    total_tests = 0

    for exercise in exercises:
        try:
            expected = build_exercise(exercise)
        except (BuildError, spec.SpecError) as err:
            failures.append(str(err))
            print(f"  FAIL  {exercise['name']}", file=sys.stderr)
            continue
        except subprocess.TimeoutExpired:
            failures.append(f"{exercise['name']}: compilation timed out")
            print(f"  FAIL  {exercise['name']}", file=sys.stderr)
            continue

        total_tests += len(expected)
        print(f"  ok    {exercise['name']:<22} {_placement(exercise):<26}"
              f"{len(expected)} tests")

        entries[exercise["name"]] = {
            "id": exercise["name"],
            "name": exercise["name"],
            "exams": exercise["exams"],
            "source": exercise["source"],
            "kind": exercise["kind"],
            "expected_files": exercise["files"],
            "allowed_functions": exercise["allowed"],
            "prototype": exercise["prototype"],
            "subject": spec.render_subject(exercise, "en"),
            "subject_th": spec.render_subject(exercise, "th"),
            "hints": exercise["hints"],
            "harness": exercise["harness"],
            "tests": expected,
        }

    if failures:
        print(f"\n{len(failures)} exercise(s) failed verification:\n", file=sys.stderr)
        for message in failures:
            print(f"* {message}\n", file=sys.stderr)
        return 1

    tracks = _index_tracks(entries)
    database = {
        "generated_by": "engine/scripts/build_db.py",
        "warning": "Generated file. Edit engine/exercises/, then rebuild.",
        "total_exercises": len(entries),
        "total_tests": total_tests,
        "tracks": tracks,
        "exercises": entries,
    }

    if args.check:
        print(
            f"\nverified {len(entries)} exercises / {total_tests} tests "
            "(database not written)"
        )
        return 0

    if args.only:
        # Writing now would replace the whole database with this one exercise.
        print("\n--only verifies but never writes; rerun without it to rebuild.")
        return 0

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print(f"\nwrote {DB_PATH}")
    print(f"{len(entries)} exercises, {total_tests} tests")
    for track, data in tracks.items():
        counts = " ".join(
            f"{level}:{len(names)}" for level, names in data["levels"].items()
        )
        print(f"  {track:<10}{data['total_levels']} levels   {counts}")
    return 0


def _placement(exercise):
    """"exam_01/5 exam_02/1", for the build log."""
    return " ".join(
        f"{track}/{level}" for track, level in sorted(exercise["exams"].items())
    )


def _index_tracks(entries):
    """Group the exercises by track and level.

    Each exercise is stored once, under `exercises`; this is the index that says
    where it appears. An exercise in two exams is placed twice and duplicated
    never -- which matters, because its level differs between them.
    """
    tracks = {}
    for track in TRACKS:
        levels = {}
        for name, entry in entries.items():
            if track in entry["exams"]:
                levels.setdefault(entry["exams"][track], []).append(name)
        if not levels:
            continue
        tracks[track] = {
            "source": EXTRA if track == EXTRA else PISCINE_2026,
            "total_levels": max(levels) + 1,
            "levels": {
                str(level): sorted(levels[level]) for level in sorted(levels)
            },
        }
    return tracks


if __name__ == "__main__":
    sys.exit(main())
