"""The five tracks: the four 2026 Piscine exams, plus a drill track.

The pack used to be one flat 0..9 ladder assigned by hand, and it disagreed with
reality -- sort_int_tab sat at level 1 when the real pool places it at exam_04
level 2. Placement now mirrors the exams themselves: an exercise records the
level it holds *within each exam it appears in*.

Those levels are not a constant offset between exams. repeat_alpha is exam_01
level 5 and exam_02 level 0; the later exams start where the earlier ones ended.
That is exactly why a single number could never describe it.

`extra` is the fifth track. It holds exercises that are not in the 2026 pool at
all and are not close enough to any exam to be worth pretending otherwise.

Between the two sits `added`: an exercise the pool does not contain but which
earns its place on an exam's ladder anyway -- ft_putchar is easier than anything
at exam_01 level 0, and exam_04 level 3 held a single exercise until eval_expr
and permutations joined it. These are placed by judgement rather than by ground
truth, so they say so wherever they are shown.
"""

EXAM_IDS = ("exam_01", "exam_02", "exam_03", "exam_04")
EXTRA = "extra"
TRACKS = EXAM_IDS + (EXTRA,)

DEFAULT_TRACK = EXAM_IDS[0]

# Where an exercise comes from, which is a different question from where it sits.
PISCINE_2026 = "piscine_2026"
ADDED = "added"
SOURCES = (PISCINE_2026, ADDED, EXTRA)


def _build_aliases():
    """`exam 02`, `exam_02`, `02` and `2` should all reach exam_02."""
    table = {EXTRA: EXTRA, "x": EXTRA, "drill": EXTRA}
    for track in EXAM_IDS:
        number = track.split("_")[1]
        for form in (
            track,
            track.replace("_", ""),
            track.replace("_", " "),
            number,
            number.lstrip("0") or "0",
        ):
            table[form] = track
    return table


ALIASES = _build_aliases()


def resolve_track(value):
    """Map user input to a track id, or None if unrecognised."""
    if not value:
        return None
    return ALIASES.get(" ".join(str(value).split()).lower().lstrip("-"))


def accepted_tracks():
    """Human-readable list of what `exam` accepts, for the error message."""
    return "01 / 02 / 03 / 04, or extra"


def track_number(track):
    """"01" for exam_01; None for the extra track."""
    return None if track == EXTRA else track.split("_")[1]
