"""The exercise pack: the source of truth for every subject and every test.

The pack itself lives in `exercises/` at the top of the repository, one
directory per exercise, in ordinary files -- see engine/pack/loader.py for the
layout and CONTRIBUTING.md for how to add one.

engine/config/ is a *generated artefact* built from that directory. Never edit
it by hand -- run `python3 engine/scripts/build_db.py`, which regenerates it and
re-verifies every reference solution on the way.
"""

import os

from engine.pack import loader, spec

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.environ.get("EXAMSHELP_PACK") or os.path.join(BASE_DIR, "exercises")


def exercise_directories(root=None):
    """Every exercise directory, by name."""
    root = root or PACK_DIR
    if not os.path.isdir(root):
        raise spec.SpecError(f"no exercise pack at {root}")
    return [
        os.path.join(root, name)
        for name in sorted(os.listdir(root))
        if not name.startswith((".", "_"))
        and os.path.isdir(os.path.join(root, name))
    ]


def load_all(root=None):
    """Every exercise in the pack, validated as a whole.

    Loading reports every broken exercise at once rather than stopping at the
    first: somebody who has just added three exercises wants all three problems,
    not three more runs.
    """
    exercises, problems = [], []
    for directory in exercise_directories(root):
        try:
            exercises.append(loader.load_exercise(directory))
        except spec.SpecError as err:
            problems.append(str(err))

    if problems:
        raise spec.SpecError(
            f"{len(problems)} exercise(s) could not be loaded:\n  "
            + "\n  ".join(problems)
        )

    spec.validate(exercises)
    # No single level to sort by: an exercise sits at a different level in each
    # exam it appears in. Order by where it is first reachable.
    exercises.sort(key=lambda e: (min(e["exams"].values()), e["name"]))
    return exercises
