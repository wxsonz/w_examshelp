"""Read one exercise from a directory of ordinary files.

The pack used to be Python: 75 exercises inside three modules, each a call to
ex() with the C source living in a triple-quoted string. That is an unkind place
to ask a C student to write C -- every backslash needs doubling, and adding one
exercise meant editing a 2,500-line file somebody else was editing too.

An exercise is now a directory:

    engine/exercises/aff_a/
        exercise.conf     placement and allowed functions
        subject.en.txt    the subject, exactly as the student reads it
        subject.th.txt
        aff_a.c           the reference solution -- a real .c file
        tests             one test per line
        hints.en.txt      hints, separated by blank lines

harness.c, stub.c and any extra reference files (ft_list.h) are optional and are
picked up by being there. Nothing is escaped, quoted or indented into a Python
literal, and `gcc engine/exercises/aff_a/aff_a.c` works from a shell.

Everything still goes through spec.ex(), so a directory and a hand-written
exercise are validated by exactly the same code.
"""

import os
import re
import shlex

from engine.pack.spec import FUNCTION, PROGRAM, SpecError, ex

CONF_FILE = "exercise.conf"
TESTS_FILE = "tests"
HARNESS_FILE = "harness.c"
STUB_FILE = "stub.c"
SUBJECT_FILES = {"en": "subject.en.txt", "th": "subject.th.txt"}
HINTS_FILE = "hints.en.txt"

# Everything exercise.conf is allowed to say. Anything else is a typo, and a
# silently ignored typo in `allowed` is a grading bug.
CONF_KEYS = ("name", "exams", "source", "allowed", "prototype", "files")

# Files in the directory that are part of the machinery rather than part of the
# solution the student submits.
NOT_SUBMITTED = {HARNESS_FILE, STUB_FILE}

_CONF_LINE = re.compile(r"^\s*([A-Za-z_]+)\s*:\s*(.*?)\s*$")
_PLACEMENT = re.compile(r"^([a-z_0-9]+)/(\d+)$")
_ESCAPES = {"t": "\t", "n": "\n", "\\": "\\"}


def load_exercise(directory):
    """Build one exercise dict from `directory`. Raises SpecError with a path."""
    name = os.path.basename(os.path.normpath(directory))

    def fail(message):
        raise SpecError(f"{os.path.join(directory, '')}: {message}")

    conf = read_conf(os.path.join(directory, CONF_FILE), fail)
    if conf.get("name", name) != name:
        fail(f"conf says name {conf['name']!r} but the directory is {name!r}")

    # Resolved before anything touches the filesystem, so a bad conf is reported
    # as a bad conf rather than as whatever file it made us go looking for.
    exams = parse_exams(conf.get("exams"), fail)

    present = sorted(
        f for f in os.listdir(directory) if f.endswith((".c", ".h"))
    )
    files = _expected_files(name, conf, present, fail)

    sources = {}
    for filename in files:
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            fail(f"expected file {filename!r} is not in the directory")
        sources[filename] = _read(path)

    stray = set(present) - set(files) - NOT_SUBMITTED
    if stray:
        fail(
            f"{', '.join(sorted(stray))} is in the directory but not in `files`, "
            "so it would never be compiled"
        )

    prototype = conf.get("prototype") or None
    subjects = {}
    for lang, filename in SUBJECT_FILES.items():
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            fail(f"missing {filename}")
        subjects[lang] = _read(path)

    tests_path = os.path.join(directory, TESTS_FILE)
    if not os.path.isfile(tests_path):
        fail(f"missing {TESTS_FILE}")

    return ex(
        name=name,
        exams=exams,
        source=conf.get("source") or "piscine_2026",
        kind=FUNCTION if prototype else PROGRAM,
        allowed=parse_list(conf.get("allowed")),
        files=files,
        prototype=prototype,
        subject=subjects["en"],
        subject_th=subjects["th"],
        reference=sources,
        harness=_optional(directory, HARNESS_FILE),
        stub=_optional(directory, STUB_FILE),
        tests=parse_tests(_read(tests_path), fail),
        hints=parse_hints(_optional(directory, HINTS_FILE) or ""),
    )


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _optional(directory, filename):
    path = os.path.join(directory, filename)
    return _read(path) if os.path.isfile(path) else None


def _expected_files(name, conf, present, fail):
    """What the student submits, in order, with `<name>.c` first.

    Derived from what is in the directory unless the conf overrides it, so the
    ft_list_* family gets its header picked up just by shipping one.
    """
    declared = parse_list(conf.get("files"))
    if declared:
        return declared

    main_file = f"{name}.c"
    if main_file not in present:
        fail(f"no {main_file} -- the reference solution is named after the exercise")
    return [main_file] + [
        f for f in present if f != main_file and f not in NOT_SUBMITTED
    ]


def read_conf(path, fail):
    if not os.path.isfile(path):
        fail(f"missing {CONF_FILE}")
    conf = {}
    for number, line in enumerate(_read(path).splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = _CONF_LINE.match(line)
        if not match:
            fail(f"{CONF_FILE} line {number} is not `key : value`: {line.strip()!r}")
        key, value = match.group(1).lower(), match.group(2)
        if key not in CONF_KEYS:
            fail(
                f"{CONF_FILE} line {number}: unknown key {key!r} "
                f"(known: {', '.join(CONF_KEYS)})"
            )
        conf[key] = value
    return conf


def parse_list(value):
    """`write, exit` -> ['write', 'exit']. Empty or absent -> []."""
    if not value:
        return []
    return [item.strip() for item in value.replace(",", " ").split() if item.strip()]


def parse_exams(value, fail):
    """`exam_01/5 exam_02/1` -> {'exam_01': 5, 'exam_02': 1}."""
    if not value:
        fail("exercise.conf must say where this sits, e.g. `exams : exam_01/5`")
    placement = {}
    for item in parse_list(value):
        match = _PLACEMENT.match(item)
        if not match:
            fail(f"{item!r} is not a placement -- write it as `exam_01/5` or `extra/2`")
        placement[match.group(1)] = int(match.group(2))
    return placement


def parse_tests(text, fail):
    """One test per line, each beginning with `$`, holding a shell-quoted argv.

    A bare `$` runs the program with no arguments, which 49 of these tests do --
    hence the sigil, so that case cannot be confused with a blank line.
    """
    tests = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith("$"):
            fail(
                f"{TESTS_FILE} line {number} does not start with `$`: {stripped!r}\n"
                "    every test line looks like `$ some args`, and a bare `$` means "
                "no arguments"
            )
        try:
            argv = shlex.split(stripped[1:], comments=True)
        except ValueError as err:
            fail(f"{TESTS_FILE} line {number} is not quoted correctly: {err}")
        tests.append([unescape(argument) for argument in argv])
    if not tests:
        fail(f"{TESTS_FILE} declares no tests")
    return tests


def parse_hints(text):
    """Hints separated by blank lines, so a long one can be wrapped."""
    hints, current = [], []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        if line.strip():
            current.append(line.strip())
        elif current:
            hints.append(" ".join(current))
            current = []
    if current:
        hints.append(" ".join(current))
    return hints


def unescape(argument):
    r"""Turn \t, \n and \\ into the bytes they name.

    Six tests pass tabs or a newline as an argument. Shell quoting alone cannot
    carry a newline on a line-per-test file, so those two get spelled out; a
    literal backslash is written `\\`.
    """
    out, i = [], 0
    while i < len(argument):
        char = argument[i]
        if char == "\\" and i + 1 < len(argument) and argument[i + 1] in _ESCAPES:
            out.append(_ESCAPES[argument[i + 1]])
            i += 2
            continue
        out.append(char)
        i += 1
    return "".join(out)


def escape(argument):
    """The inverse of unescape(), for writing a tests file."""
    return (
        argument.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
    )
