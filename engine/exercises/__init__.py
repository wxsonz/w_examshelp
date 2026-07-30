"""The exercise pack: the source of truth for every subject and every test.

engine/config/exercises_db.json is a *generated artefact* built from this
package. Never edit that file by hand -- run `python3 engine/scripts/build_db.py`
instead, which regenerates it and re-verifies every reference solution.
"""

import importlib
import pkgutil

from engine.exercises import spec


def load_all():
    """Every exercise from every rank module, validated as a whole."""
    exercises = []
    for module_info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if module_info.name.startswith("_") or module_info.name == "spec":
            continue
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        exercises.extend(getattr(module, "EXERCISES", []))

    spec.validate(exercises)
    # No single level to sort by any more: an exercise sits at a different level
    # in each exam it appears in. Order by where it is first reachable.
    exercises.sort(key=lambda e: (min(e["exams"].values()), e["name"]))
    return exercises
