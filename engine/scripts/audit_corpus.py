#!/usr/bin/env python3
"""Compare the exercise pack against a corpus of real exam subjects.

build_db.py proves the pack is *self-consistent*: subjects, references and tests
agree with each other. That is not the same as being *right*. If a subject and
its reference share a misunderstanding, everything verifies and the exercise
ships confidently wrong -- which is exactly what happened to aff_a, aff_z,
str_capitalizer, ft_countdown, lcm and ft_atoi_base until this script was run.

So this script checks the pack against outside ground truth, on five axes:

  1. behaviour   -- replays every `$> ./prog ... | cat -e` transcript from the
                    real subject and its examples.txt against our reference,
  2. structure   -- program vs function, and the exact prototype,
  3. constraints -- the allowed-functions list,
  4. coverage    -- what the corpus has that we lack, and vice versa,
  5. placement   -- which exam each exercise belongs to, and at what level.

Placement is the axis that would have caught sort_int_tab sitting at level 1 of
a flat ladder when the real pool puts it at exam_04 level 2. It makes the
levelling self-verifying rather than hand-checked.

The corpus is expected in references/ and is not part of this repository. If it
is absent the script says so and exits 0, so it is safe to run anywhere.

Usage:
    python3 engine/scripts/audit_corpus.py
    python3 engine/scripts/audit_corpus.py --corpus path/to/references
"""

import argparse
import glob
import os
import re
import shlex
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.pack import load_all, spec
from engine.scripts.build_db import compile_solution, run_test
from engine.tracks import EXTRA, PISCINE_2026

# The nigal review files concatenate subjects, each behind a ====./N-N-name.txt====
# banner. The other sources store one directory per exercise.
BLOCK = re.compile(r"=+\./[\d\-]*([a-zA-Z0-9_]+)\.txt=+\n(.*?)(?=\n=====|\Z)", re.S)

SUBJECT_FILE = re.compile(r"^subject.*\.txt$", re.I)
ENGLISH_SUBJECT = re.compile(r"^subject([._-](en|eng|english))?\.txt$", re.I)

# PISCINE_PART's layout is exam_NN/<level>/<exercise>/, and the path is the only
# place the exam and the level are written down.
PLACEMENT_PATH = re.compile(r"(exam_\d+)/(\d+)/")

# Real subjects elide long output with this marker; such a transcript is not
# comparable and must not be reported as a disagreement.
ELISION = ("[...]", "...")


def _read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def _assignment_name(body, path):
    """The exercise this subject is for.

    Keyed off the `Assignment name` field the subject itself declares, which is
    what makes the three corpus layouts -- and whatever shape references/new
    turns up in -- all load through the same code. A handful of subjects (lcm)
    ship without that header, so the directory name is the fallback.
    """
    declared = field(body, "Assignment name")
    if declared:
        return declared
    directory = os.path.dirname(path)
    if os.path.basename(directory) == "attachment":
        directory = os.path.dirname(directory)
    return re.sub(r"^[\d\-]+", "", os.path.basename(directory))


def _rank(root, path):
    """Precedence, highest wins: references/new > the 2026 exams > everything else.

    The second element demotes non-English subjects, so subject.fr.txt is only
    used where no English one exists.
    """
    relative = os.path.relpath(path, root).replace(os.sep, "/")
    if "new/" in f"{relative}/".lower():
        source = 3
    elif PLACEMENT_PATH.search(relative):
        source = 2
    else:
        source = 1
    english = 1 if ENGLISH_SUBJECT.match(os.path.basename(path)) else 0
    return (source, english)


def _entry(corpus, name):
    return corpus.setdefault(
        name,
        {"body": "", "rank": (-1, -1), "placement": {}, "examples": "", "origin": ""},
    )


def load_corpus(root):
    """Every real subject we can find, keyed by the exercise it belongs to."""
    corpus = {}

    for path in sorted(glob.glob(os.path.join(root, "nigal-*"))):
        for name, body in BLOCK.findall(_read(path)):
            entry = _entry(corpus, name)
            if entry["rank"] < (0, 1):
                entry.update(body=body, rank=(0, 1), origin=path)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for filename in sorted(filenames):
            if not SUBJECT_FILE.match(filename):
                continue
            path = os.path.join(dirpath, filename)
            body = _read(path)
            entry = _entry(corpus, _assignment_name(body, path))

            rank = _rank(root, path)
            if rank > entry["rank"]:
                entry.update(body=body, rank=rank, origin=path)

            # Placement accumulates from every copy: an exercise legitimately
            # appears in more than one exam, at a different level in each.
            found = PLACEMENT_PATH.search(
                os.path.relpath(path, root).replace(os.sep, "/")
            )
            if found:
                entry["placement"][found.group(1)] = int(found.group(2))

            examples = _find_examples(path)
            if examples and not entry["examples"]:
                entry["examples"] = examples

    return {name: entry for name, entry in corpus.items() if entry["body"]}


def _find_examples(subject_path):
    """examples.txt sits either beside the subject or one directory up."""
    directory = os.path.dirname(subject_path)
    for candidate in (
        os.path.join(directory, "examples.txt"),
        os.path.join(os.path.dirname(directory), "examples.txt"),
    ):
        if os.path.isfile(candidate):
            return _read(candidate)
    return ""


def field(body, label):
    match = re.search(rf"^{label}\s*:(.*)$", body, re.M)
    return match.group(1).strip() if match else None


def real_prototype(body, name):
    for line in body.splitlines():
        text = line.strip()
        if re.search(rf"\b{name}\s*\(", text) and text.endswith(";"):
            return re.sub(r"\s+", " ", text)
    return None


def transcripts(body, name):
    """Yield (argv, expected_lines) for comparable `| cat -e` sessions."""
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        text = raw.strip()
        if not text.startswith("$>"):
            i += 1
            continue
        command = text[2:].strip()
        if "| cat -e" not in command:
            i += 1
            continue
        command = command.split("|")[0].strip()
        try:
            argv = shlex.split(command)
        except ValueError:
            i += 1
            continue
        if not argv or argv[0] != f"./{name}":
            i += 1
            continue

        indent = " " * (len(raw) - len(raw.lstrip()))
        i += 1
        output, elided = [], False
        while i < len(lines):
            candidate = lines[i]
            candidate = (
                candidate[len(indent):]
                if candidate.startswith(indent)
                else candidate.lstrip()
            )
            if candidate.strip().startswith("$>") or not candidate.endswith("$"):
                break
            content = candidate[:-1]
            if content.strip() in ELISION:
                elided = True
            output.append(content)
            i += 1
        if not elided:
            yield argv[1:], output


def _show_placement(placement):
    return " ".join(f"{exam}/{level}" for exam, level in sorted(placement.items())) or "(nowhere)"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        default=os.path.join(BASE_DIR, "references"),
        help="directory holding the reference exam material",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.corpus):
        print(f"no corpus at {args.corpus} -- nothing to audit against.")
        return 0

    corpus = load_corpus(args.corpus)
    pack = {e["name"]: e for e in load_all()}
    if not corpus:
        print(f"corpus at {args.corpus} contained no recognisable subjects.")
        return 0

    print(f"corpus: {len(corpus)} real subjects   pack: {len(pack)} exercises\n")

    problems = []
    agreed = []
    unverifiable = []

    for name, exercise in sorted(pack.items()):
        entry = corpus.get(name)
        if not entry:
            continue
        body = entry["body"]

        # --- placement -----------------------------------------------------
        placement = entry["placement"]
        if placement:
            if exercise["source"] == PISCINE_2026:
                ours = {k: v for k, v in exercise["exams"].items() if k != EXTRA}
                if ours != placement:
                    problems.append(
                        (name, "placement",
                         f"corpus: {_show_placement(placement)}\n"
                         f"              ours:   {_show_placement(ours)}")
                    )
            else:
                problems.append(
                    (name, "placement",
                     f"filed as {exercise['source']!r} but the 2026 pool has it at "
                     f"{_show_placement(placement)}")
                )

        # --- structure -----------------------------------------------------
        proto = real_prototype(body, name)
        if proto and exercise["kind"] == spec.PROGRAM:
            problems.append((name, "structure", f"corpus declares a function: {proto}"))
        elif proto and exercise["prototype"]:
            a = re.sub(r"\s+", "", proto).rstrip(";")
            b = re.sub(r"\s+", "", exercise["prototype"]).rstrip(";")
            if a != b:
                problems.append(
                    (name, "prototype", f"corpus: {proto}\n              ours:   {exercise['prototype']}")
                )
        elif not proto and exercise["kind"] == spec.FUNCTION:
            problems.append((name, "structure", "corpus shows no prototype (likely a program)"))

        # --- constraints ---------------------------------------------------
        allowed = field(body, "Allowed functions")
        if allowed is not None:
            real_set = {
                a.strip().lower()
                for a in allowed.split(",")
                if a.strip() and a.strip().lower() not in ("none", "-")
            }
            ours = {a.strip().lower() for a in exercise["allowed"]}
            if real_set != ours:
                problems.append(
                    (name, "allowed",
                     f"corpus: {', '.join(sorted(real_set)) or '(none)'}\n"
                     f"              ours:   {', '.join(sorted(ours)) or '(none)'}")
                )

        # --- behaviour -----------------------------------------------------
        # examples.txt is already in `$> ./prog ... | cat -e` form, so it feeds
        # the same replay as the subject's own transcripts.
        cases = list(transcripts(body, name)) + list(
            transcripts(entry["examples"], name)
        )
        if not cases:
            unverifiable.append(name)
            continue
        with tempfile.TemporaryDirectory() as work_dir:
            try:
                binary = compile_solution(
                    work_dir, exercise, spec.reference_sources(exercise), "reference"
                )
            except Exception as err:
                problems.append((name, "compile", str(err).splitlines()[0]))
                continue
            mismatched = []
            for argv, want in cases:
                try:
                    got, _ = run_test(binary, {"argv": argv, "stdin": ""})
                except subprocess.TimeoutExpired:
                    mismatched.append((argv, want, ["<timed out>"]))
                    continue
                got_lines = got.split("\n")
                if got_lines and got_lines[-1] == "":
                    got_lines.pop()
                if got_lines != want:
                    mismatched.append((argv, want, got_lines))
            if mismatched:
                detail = "\n".join(
                    f"              argv={argv}\n"
                    f"                corpus: {want}\n"
                    f"                ours:   {got}"
                    for argv, want, got in mismatched[:3]
                )
                problems.append((name, "behaviour", "\n" + detail))
            else:
                agreed.append((name, len(cases)))

    print(f"{len(agreed)} exercises match the corpus examples exactly")
    if agreed:
        print("   " + ", ".join(f"{n}({c})" for n, c in agreed))

    if unverifiable:
        print(f"\n{len(unverifiable)} in corpus but with no comparable `| cat -e` "
              "examples (checked on structure and constraints only)")
        print("   " + ", ".join(sorted(unverifiable)))

    mine_only = sorted(set(pack) - set(corpus))
    corpus_only = sorted(n for n in set(corpus) - set(pack) if n.isidentifier())
    print(f"\n{len(mine_only)} pack exercises are not in this corpus "
          "(may be from another rank's pool, or invented)")
    print("   " + ", ".join(mine_only))
    print(f"\n{len(corpus_only)} corpus exercises are missing from the pack")
    print("   " + ", ".join(corpus_only))

    if problems:
        print(f"\n{len(problems)} DISAGREEMENT(S) WITH GROUND TRUTH\n")
        for name, kind, detail in problems:
            print(f"  {name} [{kind}] {detail}")
        return 1

    print("\nNo disagreements with the corpus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
