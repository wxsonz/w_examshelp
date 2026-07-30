"""Schema for the exercise pack.

Every exercise here carries a reference solution. Expected outputs are never
written by hand: engine/scripts/build_db.py compiles the reference, runs it
against the declared inputs, and records what it printed. A subject and its
tests therefore cannot drift apart.

The build also compiles a do-nothing *stub* for each exercise and requires it to
fail. That is what keeps the grader honest -- the old database shipped 105
exercises whose every test expected `null`, so `int main(void){return 0;}`
scored "All 3/3 tests passed".
"""

import re

from engine.textwidth import display_width, pad
from engine.tracks import ADDED, EXTRA, PISCINE_2026, SOURCES, TRACKS

PROGRAM = "program"
FUNCTION = "function"

RULE_WIDTH = 80


class SpecError(Exception):
    """Raised for a malformed exercise definition."""


def ex(
    name,
    exams,
    kind,
    allowed,
    subject,
    subject_th,
    reference,
    tests,
    source=PISCINE_2026,
    files=None,
    prototype=None,
    harness=None,
    hints=(),
    stub=None,
):
    """Declare one exercise. Returns a plain dict; see module docstring.

    `exams` maps a track id to the level the exercise holds *in that track*, so
    an exercise that appears in several exams is declared once and placed
    several times.
    """
    if kind not in (PROGRAM, FUNCTION):
        raise SpecError(f"{name}: kind must be {PROGRAM!r} or {FUNCTION!r}")
    if kind == FUNCTION and not prototype:
        raise SpecError(f"{name}: function exercises need a prototype")
    if kind == FUNCTION and not harness:
        raise SpecError(f"{name}: function exercises need a harness main()")
    if kind == PROGRAM and harness:
        raise SpecError(f"{name}: program exercises must not define a harness")
    if not isinstance(exams, dict) or not exams:
        raise SpecError(f"{name}: exams must be a non-empty {{track: level}} mapping")
    for track, level in exams.items():
        if track not in TRACKS:
            raise SpecError(f"{name}: unknown track {track!r}")
        if not isinstance(level, int) or level < 0:
            raise SpecError(f"{name}: level {level!r} in {track} is not a level number")
    if source not in SOURCES:
        raise SpecError(f"{name}: source must be one of {', '.join(SOURCES)}")
    if not tests:
        raise SpecError(f"{name}: at least one test is required")

    return {
        "name": name,
        "exams": dict(exams),
        "source": source,
        "kind": kind,
        "files": list(files) if files else [f"{name}.c"],
        "allowed": list(allowed),
        "prototype": prototype,
        "subject": subject.strip("\n"),
        "subject_th": subject_th.strip("\n"),
        "reference": reference,
        "harness": harness,
        "hints": list(hints),
        "stub": stub,
        "tests": [_norm_test(name, t) for t in tests],
    }


def reference_sources(exercise):
    """The reference solution as a {filename: source} mapping.

    An exercise may declare `reference` as a single string (written to the first
    expected file) or as a dict, which is how multi-file exercises such as the
    ft_list_* family ship their header alongside the .c file.
    """
    ref = exercise["reference"]
    if isinstance(ref, dict):
        return dict(ref)
    return {exercise["files"][0]: ref}


def _norm_test(ex_name, t):
    if isinstance(t, (list, tuple)):
        t = {"argv": list(t)}
    argv = [str(a) for a in t.get("argv", [])]
    return {
        "argv": argv,
        "stdin": t.get("stdin", ""),
        "note": t.get("note", ""),
    }


# --------------------------------------------------------------------------
# Subject rendering
# --------------------------------------------------------------------------

_HEADERS = {
    "en": ("Assignment name", "Expected files", "Allowed functions"),
    "th": ("ชื่อโจทย์", "ไฟล์ที่ต้องส่ง", "ฟังก์ชันที่ใช้ได้"),
}


def render_subject(exercise, lang="en", rule_width=RULE_WIDTH):
    """Compose an authentic 42-style subject block.

    The header is always derived from the exercise metadata, so it can never
    contradict what `status` reports or what the grader looks for.
    """
    labels = list(_HEADERS.get(lang, _HEADERS["en"]))
    labels.append("Prototype" if lang == "en" else "ต้นแบบฟังก์ชัน")
    body = exercise["subject_th"] if lang == "th" else exercise["subject"]

    # Pad by display width, not len(): Thai labels are full of combining marks.
    width = max(display_width(label) for label in labels)
    values = [
        exercise["name"],
        ", ".join(exercise["files"]),
        ", ".join(exercise["allowed"]) or "None",
    ]
    if exercise["prototype"]:
        values.append(exercise["prototype"])

    lines = [f"{pad(label, width)} : {value}" for label, value in zip(labels, values)]
    lines += ["-" * rule_width, "", body]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Prototype parsing -- used to synthesise stub solutions for the build's
# honesty check, and to validate that a submission declares what it promises.
# --------------------------------------------------------------------------


def parse_prototype(proto):
    """Split a C prototype into (return_type, name, [(type, name), ...])."""
    text = proto.strip().rstrip(";").strip()
    try:
        open_paren = text.index("(")
        close_paren = text.rindex(")")
    except ValueError:
        raise SpecError(f"cannot parse prototype: {proto!r}")

    head = text[:open_paren]
    m = re.search(r"([A-Za-z_]\w*)\s*$", head)
    if not m:
        raise SpecError(f"cannot find function name in: {proto!r}")

    fn_name = m.group(1)
    ret_type = head[: m.start()].strip()
    params = [p.strip() for p in _split_params(text[open_paren + 1 : close_paren])]
    params = [p for p in params if p and p != "void"]
    return ret_type, fn_name, [(p, _param_name(p)) for p in params]


def _split_params(text):
    """Split on commas that are not nested inside parentheses or brackets."""
    out, depth, current = [], 0, ""
    for ch in text:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(current)
            current = ""
        else:
            current += ch
    out.append(current)
    return out


def _param_name(param):
    """Best-effort identifier for a parameter, or None if unnamed."""
    # Function pointers: the name sits inside the first parenthesised group.
    fp = re.search(r"\(\s*\*\s*([A-Za-z_]\w*)\s*\)", param)
    if fp:
        return fp.group(1)
    stripped = re.sub(r"\[[^\]]*\]", "", param).strip()
    m = re.search(r"([A-Za-z_]\w*)\s*$", stripped)
    if not m:
        return None
    candidate = m.group(1)
    # A bare type such as `char *` or `unsigned int` has no parameter name.
    remainder = stripped[: m.start()].strip()
    if not remainder:
        return None
    return candidate


_INT_TYPES = ("int", "char", "long", "short", "size_t", "unsigned", "_Bool")


def make_stub(exercise):
    """C source for a syntactically valid solution that does nothing useful.

    The build requires this to FAIL grading; if it passes, the exercise has no
    real assertions and must not ship.
    """
    if exercise["stub"] is not None:
        return exercise["stub"]

    if exercise["kind"] == PROGRAM:
        return "int main(void)\n{\n\treturn (0);\n}\n"

    ret_type, fn_name, params = parse_prototype(exercise["prototype"])
    body = []
    for i, (ptype, pname) in enumerate(params):
        if pname:
            body.append(f"\t(void){pname};")
        else:
            raise SpecError(
                f"{exercise['name']}: parameter {i + 1} of the prototype is unnamed, "
                "so no stub can be synthesised -- pass stub= explicitly"
            )

    if ret_type.replace(" ", "") == "void":
        pass
    elif "*" in ret_type:
        body.append("\treturn (0);")
    elif any(t in ret_type for t in _INT_TYPES):
        body.append("\treturn (0);")
    else:
        raise SpecError(
            f"{exercise['name']}: unknown return type {ret_type!r} -- pass stub= explicitly"
        )

    return f"{exercise['prototype'].rstrip(';')}\n{{\n" + "\n".join(body) + "\n}\n"


def validate(exercises):
    """Check pack-level invariants. Raises SpecError on the first problem."""
    seen = {}
    for e in exercises:
        if e["name"] in seen:
            raise SpecError(f"duplicate exercise name: {e['name']}")
        seen[e["name"]] = e

        # The drill track and the drill source imply each other; anything with a
        # place on an exam ladder must say which one it is.
        tracks = set(e["exams"])
        if e["source"] == EXTRA and tracks != {EXTRA}:
            raise SpecError(
                f"{e['name']}: source is {EXTRA!r} but it claims "
                f"{', '.join(sorted(tracks - {EXTRA}))} -- drill-only exercises live "
                f"in the {EXTRA} track. Placing it on an exam makes it {ADDED!r}."
            )
        if e["source"] != EXTRA and EXTRA in tracks:
            raise SpecError(
                f"{e['name']}: source is {e['source']!r} but it sits in the "
                f"{EXTRA} track"
            )

        sources = reference_sources(e)
        for filename in sources:
            if filename not in e["files"]:
                raise SpecError(
                    f"{e['name']}: reference provides {filename!r}, which is not in "
                    f"the expected files {e['files']}"
                )
        joined = "\n".join(sources.values())

        if e["kind"] == FUNCTION:
            _, fn_name, _ = parse_prototype(e["prototype"])
            if fn_name != e["name"]:
                raise SpecError(
                    f"{e['name']}: prototype declares {fn_name!r}, which does not "
                    "match the exercise name"
                )
            if re.search(r"\bmain\s*\(", joined):
                raise SpecError(
                    f"{e['name']}: reference solution for a function exercise must "
                    "not define main() -- that belongs in the harness"
                )
        else:
            if not re.search(r"\bmain\s*\(", joined):
                raise SpecError(
                    f"{e['name']}: reference solution for a program exercise must "
                    "define main()"
                )

    _validate_ladders(exercises)
    return seen


def _validate_ladders(exercises):
    """Each track must be a ladder with no missing rung.

    A typo that puts an exercise at level 9 of a four-level exam would otherwise
    strand the student on an empty level with nothing left to solve.
    """
    for track in TRACKS:
        levels = sorted(
            {e["exams"][track] for e in exercises if track in e["exams"]}
        )
        if not levels:
            continue
        if levels != list(range(len(levels))):
            missing = sorted(set(range(max(levels) + 1)) - set(levels))
            raise SpecError(
                f"{track}: levels must run 0..{max(levels)} with no gaps; "
                f"nothing sits at level(s) {', '.join(map(str, missing))}"
            )
