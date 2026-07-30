#!/usr/bin/env python3
"""Stamp out a new exercise directory that already builds.

The skeleton is a working exercise, not a set of blanks: it compiles, its tests
run, and its stub fails. So you can run build_db.py straight away, see it pass,
and then change one thing at a time -- which is a much better place to start
than an empty directory and a format you have not read yet.

Usage:
    python3 engine/scripts/new_exercise.py alen --exams exam_01/4
    python3 engine/scripts/new_exercise.py title --exams exam_02/3 \\
        --prototype "void title(char *str);"
"""

import argparse
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.pack import PACK_DIR
from engine.pack.loader import CONF_FILE, HARNESS_FILE, HINTS_FILE, TESTS_FILE

CONF = """\
# Where this sits. `exam_01/4` means exam 01, level 4. An exercise can be in
# several exams at different levels: `exams : exam_01/5 exam_02/1`.
exams     : {exams}

# Where it comes from. Leave this out if it is a real 2026 pool exercise.
# `added` = not in the pool, but placed on an exam ladder by difficulty.
# `extra` = drill only; then the only placement allowed is `extra/N`.
{source}
# Everything the student is allowed to call, comma separated. Empty means
# nothing at all -- not even write().
allowed   : write
{prototype}"""

SUBJECT_EN = """\
Write a program that ... .

Say exactly what is printed, including whether it ends with a newline: the
grader compares bytes.

Examples:

  $> ./{name} hello | cat -e
  hello$
"""

SUBJECT_TH = """\
เขียนโปรแกรมที่ ...

ระบุให้ชัดเจนว่าต้องแสดงผลอะไรบ้าง รวมถึงว่าจบด้วยการขึ้นบรรทัดใหม่หรือไม่
เพราะตัวตรวจเทียบผลลัพธ์ทีละไบต์

ตัวอย่าง:

  $> ./{name} hello | cat -e
  hello$
"""

PROGRAM_REFERENCE = """\
#include <unistd.h>

int\tmain(int argc, char **argv)
{{
\tint\ti;

\tif (argc != 2)
\t\treturn (0);
\ti = 0;
\twhile (argv[1][i])
\t\twrite(1, &argv[1][i++], 1);
\twrite(1, "\\n", 1);
\treturn (0);
}}
"""

FUNCTION_REFERENCE = """\
#include <unistd.h>

{prototype_body}
{{
\twhile (*{argument})
\t\twrite(1, {argument}++, 1);
}}
"""

FUNCTION_HARNESS = """\
#include <unistd.h>

{prototype}

int\tmain(int argc, char **argv)
{{
\tint\ti;

\ti = 1;
\twhile (i < argc)
\t{{
\t\t{name}(argv[i]);
\t\twrite(1, "\\n", 1);
\t\ti++;
\t}}
\treturn (0);
}}
"""

TESTS = """\
# One test per line. The line is the argv, shell-quoted; a bare `$` runs the
# program with no arguments at all. Use \\t and \\n for a tab or a newline
# inside an argument. Anything after `#` is a comment.
#
# You do NOT write the expected output anywhere: the build runs your reference
# solution and records what it actually printed.
$ hello
$ 'two words'
$ ''
$
"""

HINTS = """\
Hints are separated by blank lines, so a long one can be wrapped across
several lines like this one.

Say what to watch out for, not how to solve it.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="the exercise name, e.g. alen")
    parser.add_argument("--exams", default="exam_01/0",
                        help="placement, e.g. 'exam_01/5 exam_02/1' (default: exam_01/0)")
    parser.add_argument("--source", choices=("piscine_2026", "added", "extra"),
                        default="piscine_2026", help="default: piscine_2026")
    parser.add_argument("--prototype",
                        help="makes it a function exercise, e.g. 'void ft_putstr(char *str);'")
    parser.add_argument("--pack", default=PACK_DIR, help="where the pack lives")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z_][a-z0-9_]*", args.name):
        print(f"{args.name!r} is not a usable exercise name (lowercase, digits, "
              "underscores)", file=sys.stderr)
        return 1

    directory = os.path.join(args.pack, args.name)
    if os.path.exists(directory):
        print(f"{directory} already exists", file=sys.stderr)
        return 1
    os.makedirs(directory)

    written = []

    def write(filename, text):
        with open(os.path.join(directory, filename), "w", encoding="utf-8") as f:
            f.write(text)
        written.append(filename)

    source_line = (
        "" if args.source == "piscine_2026" else f"source    : {args.source}\n"
    )
    prototype_line = (
        f"\n# Present = this is a function exercise, and harness.c must call it.\n"
        f"prototype : {args.prototype}\n"
        if args.prototype
        else ""
    )
    write(CONF_FILE, CONF.format(exams=args.exams, source=source_line,
                                 prototype=prototype_line))
    write("subject.en.txt", SUBJECT_EN.format(name=args.name))
    write("subject.th.txt", SUBJECT_TH.format(name=args.name))

    if args.prototype:
        body = args.prototype.strip().rstrip(";")
        argument = _first_argument(args.prototype) or "str"
        write(f"{args.name}.c",
              FUNCTION_REFERENCE.format(prototype_body=body, argument=argument))
        write(HARNESS_FILE,
              FUNCTION_HARNESS.format(prototype=args.prototype.strip().rstrip(";") + ";",
                                      name=args.name))
    else:
        write(f"{args.name}.c", PROGRAM_REFERENCE)

    write(TESTS_FILE, TESTS)
    write(HINTS_FILE, HINTS)

    print(f"created {directory}/")
    for filename in written:
        print(f"  {filename}")
    print(
        "\nThe skeleton already builds. Check it, then change it:\n"
        f"    python3 engine/scripts/build_db.py --only {args.name}"
    )
    return 0


def _first_argument(prototype):
    """The name of the first parameter, for the placeholder body."""
    inside = prototype[prototype.find("(") + 1 : prototype.rfind(")")]
    match = re.search(r"([A-Za-z_]\w*)\s*$", inside.split(",")[0].strip())
    return match.group(1) if match else None


if __name__ == "__main__":
    sys.exit(main())
