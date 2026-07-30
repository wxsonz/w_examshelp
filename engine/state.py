import os
import json
import difflib
import random
from engine.i18n import resolve_language
from engine.session import SessionManager
from engine.tracks import DEFAULT_TRACK, TRACKS, resolve_track

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(ENGINE_DIR, "config", "exercises_db.json")
ROOT_DIR = os.path.dirname(ENGINE_DIR)
STATE_FILE = os.path.join(ROOT_DIR, ".examshelp_state.json")

class StateManager:
    def __init__(self, workspace_subjects=None, workspace_rendu=None,
                 state_file=None, history_dir=None):
        # The three locations are overridable by environment variable so a test
        # run cannot clobber real progress, and so a user can relocate their
        # workspace without moving the install.
        self.workspace_subjects = (
            workspace_subjects
            or os.environ.get("EXAMSHELP_SUBJECTS")
            or os.path.join(ROOT_DIR, "subjects")
        )
        self.workspace_rendu = (
            workspace_rendu
            or os.environ.get("EXAMSHELP_RENDU")
            or os.path.join(ROOT_DIR, "rendu")
        )
        self.state_file = (
            state_file or os.environ.get("EXAMSHELP_STATE") or STATE_FILE
        )
        self.session_mgr = SessionManager(
            history_dir=(
                history_dir
                or os.environ.get("EXAMSHELP_HISTORY")
                or os.path.join(ROOT_DIR, "history")
            ),
            rendu_dir=self.workspace_rendu,
            subjects_dir=self.workspace_subjects
        )
        
        self.db = self._load_db()
        self.state = self._load_state()
        
        self.health_check()

    def _load_db(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"total_exercises": 0, "tracks": {}, "exercises": {}}

    def has_exercises(self):
        return bool(self.db.get("exercises"))

    def _load_state(self):
        new_session_name = SessionManager.generate_cute_session_name()
        state = {
            "session_name": new_session_name,
            "current_track": DEFAULT_TRACK,
            "progress": {},
            "completed_exercises": [],
            "session_completed": [],
            "total_completions": 0,
            "language": "en",
            "history": []
        }

        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        last_session = data.get("session_name")
                        archived_status = data.get("session_archived", False)

                        state.update(data)

                        # When a new session starts, reset per-session completion counter
                        if archived_status or not last_session:
                            state["session_name"] = new_session_name
                            state["session_archived"] = False
                            state["session_completed"] = []
                            for entry in state.get("progress", {}).values():
                                if isinstance(entry, dict):
                                    entry["active"] = None
            except Exception:
                pass

        if "session_completed" not in state:
            state["session_completed"] = []
        if "total_completions" not in state:
            state["total_completions"] = len(state.get("completed_exercises", []))

        return self._migrate(state)

    def _migrate(self, state):
        """Bring a pre-exam state file forward.

        Level numbers changed meaning when the pack stopped being one flat
        ladder: level 1 used to hold sort_int_tab, which the real pool places at
        exam_04 level 2. So the old integer is dropped rather than carried over.
        Completed exercises are kept -- those are names, and names still mean the
        same thing -- and each track's level is recomputed from them on first use.
        """
        state.pop("current_level", None)
        state.pop("active_exercise_id", None)
        if not isinstance(state.get("progress"), dict):
            state["progress"] = {}
        if resolve_track(state.get("current_track")) is None:
            state["current_track"] = DEFAULT_TRACK
        return state

    # ------------------------------------------------------------- the tracks

    def _track_index(self):
        return self.db.get("tracks", {})

    def available_tracks(self):
        """Track ids the database actually holds, in ladder order."""
        return [track for track in TRACKS if track in self._track_index()]

    def get_current_track(self):
        track = self.state.get("current_track")
        if track in self._track_index():
            return track
        available = self.available_tracks()
        return available[0] if available else DEFAULT_TRACK

    def set_current_track(self, value):
        """Switch exam. Accepts `02`, `exam_02`, `exam 02`, `extra`.

        Returns the track id, or None if it is not one we have.
        """
        track = resolve_track(value)
        if track is None or track not in self._track_index():
            return None
        self.state["current_track"] = track
        self._track_progress(track)
        self.save_state()
        self._sync_current_subject()
        return track

    def track_levels(self, track):
        return self._track_index().get(track, {}).get("levels", {})

    def track_total_levels(self, track):
        return self._track_index().get(track, {}).get("total_levels", 0)

    def track_exercise_names(self, track):
        """Every exercise in a track, deduplicated across its levels."""
        names = set()
        for level_names in self.track_levels(track).values():
            names.update(level_names)
        return names

    def exercises_at(self, track, level):
        catalogue = self.db.get("exercises", {})
        return [
            catalogue[name]
            for name in self.track_levels(track).get(str(level), [])
            if name in catalogue
        ]

    def _track_progress(self, track):
        """This track's {level, active}, created and repaired on demand."""
        progress = self.state.setdefault("progress", {})
        entry = progress.get(track)
        if not isinstance(entry, dict):
            entry = {"level": self.first_unfinished_level(track), "active": None}
            progress[track] = entry

        level = entry.get("level")
        if not isinstance(level, int) or level < 0:
            level = 0
        entry["level"] = min(level, max(self.track_total_levels(track) - 1, 0))
        entry.setdefault("active", None)
        return entry

    def first_unfinished_level(self, track):
        """The lowest level still holding something uncompleted."""
        completed = set(self.state.get("completed_exercises", []))
        levels = self.track_levels(track)
        for key in sorted(levels, key=int):
            if any(name not in completed for name in levels[key]):
                return int(key)
        return max(self.track_total_levels(track) - 1, 0)

    def track_summary(self):
        """Per-track progress for the `exam` command. Does not mutate state."""
        completed = set(self.state.get("completed_exercises", []))
        current = self.get_current_track()
        rows = []
        for track in self.available_tracks():
            names = self.track_exercise_names(track)
            entry = self.state.get("progress", {}).get(track)
            level = entry.get("level") if isinstance(entry, dict) else None
            if not isinstance(level, int):
                level = self.first_unfinished_level(track)
            rows.append({
                "track": track,
                "source": self._track_index()[track].get("source", ""),
                "level": level,
                "total_levels": self.track_total_levels(track),
                "done": len(names & completed),
                "total": len(names),
                "current": track == current,
            })
        return rows

    def reset_all_progress(self):
        """Resets all cumulative and per-session progress back to 0."""
        self.state["current_track"] = (self.available_tracks() or [DEFAULT_TRACK])[0]
        self.state["progress"] = {}
        self.state["completed_exercises"] = []
        self.state["session_completed"] = []
        self.state["total_completions"] = 0
        self.state["session_name"] = SessionManager.generate_cute_session_name()
        self.save_state()
        self.session_mgr.clean_workspace()
        self._select_random_exercise_for_level()
        self.save_state()
        self._sync_current_subject()

    def health_check(self):
        os.makedirs(self.workspace_subjects, exist_ok=True)
        os.makedirs(self.workspace_rendu, exist_ok=True)

        self.state["current_track"] = self.get_current_track()
        self._track_progress(self.state["current_track"])

        active_ex = self.get_current_exercise()
        if not active_ex:
            self._select_random_exercise_for_level()

        self.save_state()
        self._sync_current_subject()

    def save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def get_session_name(self):
        return self.state.get("session_name", "cute-session")

    def get_language(self):
        return self.state.get("language", "en")

    def set_language(self, lang):
        """Switch language and rewrite subjects/. Returns the code set, or None.

        Accepts aliases, so `thai` and `english` work as well as `th` and `en`.
        """
        code = resolve_language(lang)
        if not code:
            return None
        self.state["language"] = code
        self.save_state()
        self._sync_current_subject()
        return code

    def get_level(self, track):
        return self._track_progress(track)["level"]

    def get_active_name(self, track):
        return self._track_progress(track).get("active")

    def get_current_level(self):
        return self.get_level(self.get_current_track())

    def get_current_exercise(self):
        track = self.get_current_track()
        entry = self._track_progress(track)
        level_exs = self.exercises_at(track, entry["level"])
        if not level_exs:
            return None

        active = entry.get("active")
        if active:
            for ex in level_exs:
                if ex["name"] == active:
                    return ex

        return self._select_random_exercise_for_level()

    def _select_random_exercise_for_level(self):
        track = self.get_current_track()
        entry = self._track_progress(track)
        level_exs = self.exercises_at(track, entry["level"])
        if not level_exs:
            entry["active"] = None
            return None

        completed = set(self.state.get("completed_exercises", []))
        uncompleted = [ex for ex in level_exs if ex["name"] not in completed]

        chosen = random.choice(uncompleted or level_exs)
        entry["active"] = chosen["name"]
        return chosen

    # ------------------------------------------------------- jumping straight

    def exercise_names(self):
        return sorted(self.db.get("exercises", {}))

    def match_exercise(self, target):
        """Resolve what was typed to one exercise name.

        Returns (name, candidates, kind). A name means we know what was meant.
        Otherwise `kind` says why we do not, and the two reasons want different
        wording: "ambiguous" is a fragment that fits several exercises and the
        fix is to type more, while "similar" is a typo and the fix is to pick
        one of the guesses.

        An unambiguous fragment counts as a match, so `fizz` finds fizzbuzz and
        nobody has to type ft_list_push_front in full.
        """
        needle = (target or "").strip().lower()
        if not needle:
            return None, [], "empty"

        names = self.exercise_names()
        for name in names:
            if name.lower() == needle:
                return name, [], "exact"

        contains = [name for name in names if needle in name.lower()]
        if len(contains) == 1:
            return contains[0], [], "fragment"
        if contains:
            return None, contains, "ambiguous"

        # Nothing contains it, so this is a typo rather than an abbreviation.
        # difflib ranks by whole-string similarity, which is the right question
        # to ask once substring matching has already come up empty.
        return None, difflib.get_close_matches(needle, names, n=3, cutoff=0.5), "similar"

    def jump_to_exercise(self, name):
        """Make `name` current, moving track and level as far as it takes.

        Returns the exercise, or None if there is no such name. An exercise that
        appears in several exams is reached through the current one where
        possible, so jumping does not silently move you off the exam you are on.
        """
        exercise = self.db.get("exercises", {}).get(name)
        if not exercise:
            return None

        exams = exercise.get("exams") or {}
        track = self.get_current_track()
        if track not in exams:
            track = next((t for t in TRACKS if t in exams), None)
        if track is None:
            return None

        self.state["current_track"] = track
        entry = self._track_progress(track)
        entry["level"] = exams[track]
        entry["active"] = name
        self.save_state()
        self._sync_current_subject()
        return exercise

    def complete_current_exercise(self):
        ex = self.get_current_exercise()
        if ex:
            if ex["name"] not in self.state["completed_exercises"]:
                self.state["completed_exercises"].append(ex["name"])
            self.state["session_completed"].append(ex["name"])
            self.state["total_completions"] = self.state.get("total_completions", 0) + 1
                
        self._advance_exercise()

    def skip_current_exercise(self):
        ex = self.get_current_exercise()
        old_name = ex["name"] if ex else "unknown"
        self._advance_exercise()
        new_ex = self.get_current_exercise()
        return old_name, new_ex

    def _advance_exercise(self):
        track = self.get_current_track()
        entry = self._track_progress(track)
        level_exs = self.exercises_at(track, entry["level"])
        completed = set(self.state.get("completed_exercises", []))

        uncompleted = [ex for ex in level_exs if ex["name"] not in completed]
        current = entry.get("active")
        different_candidates = [ex for ex in uncompleted if ex["name"] != current]

        if different_candidates:
            entry["active"] = random.choice(different_candidates)["name"]
        elif uncompleted:
            entry["active"] = uncompleted[0]["name"]
        # The ceiling is per-exam: exam_01 has eight levels, exam_04 has four.
        elif entry["level"] + 1 < self.track_total_levels(track):
            entry["level"] += 1
            self._select_random_exercise_for_level()
        elif level_exs:
            entry["active"] = random.choice(level_exs)["name"]

        self.save_state()
        self._sync_current_subject()

    def workspace_has_code(self):
        """True if the student has anything in rendu/ worth archiving."""
        for _, _, files in os.walk(self.workspace_rendu):
            if files:
                return True
        return False

    def archive_current_session(self, clean_workspace=False):
        """Snapshot rendu/ and subjects/ into history/.

        clean_workspace defaults to False: quitting used to delete the student's
        work from rendu/, which is a nasty surprise if you exit mid-exercise just
        to look something up. `reset` still clears it, deliberately.
        """
        current_name = self.get_session_name()
        if not self.workspace_has_code():
            return None, {"session_name": current_name}

        folder, meta = self.session_mgr.archive_session(current_name, self.state)

        if clean_workspace:
            self.session_mgr.clean_workspace()

        self.state["session_archived"] = True
        self.state["session_name"] = SessionManager.generate_cute_session_name()
        self.state["session_completed"] = []
        self.save_state()

        return folder, meta

    def _sync_current_subject(self):
        """Write the current subject to subjects/ in both languages."""
        os.makedirs(self.workspace_subjects, exist_ok=True)
        ex = self.get_current_exercise()
        if not ex:
            return

        fallback = f"Assignment name : {ex['name']}\n"
        texts = {
            "en": ex.get("subject") or fallback,
            "th": ex.get("subject_th") or ex.get("subject") or fallback,
        }
        for lang, text in texts.items():
            for filename in (f"subject_{ex['name']}.{lang}.txt", f"subject.{lang}.txt"):
                with open(
                    os.path.join(self.workspace_subjects, filename), "w",
                    encoding="utf-8",
                ) as f:
                    f.write(text)

    def get_progress_data(self):
        track = self.get_current_track()
        return {
            "session_name": self.get_session_name(),
            "track": track,
            "current_level": self.get_current_level(),
            "total_levels": self.track_total_levels(track),
            "session_completed_count": len(self.state.get("session_completed", [])),
            "total_completions": self.state.get("total_completions", 0),
            "total_count": self.db.get("total_exercises", 0),
            "language": self.get_language(),
            "current_exercise": self.get_current_exercise(),
        }
