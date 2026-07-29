import os
import json
import random
from engine.session import SessionManager

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(ENGINE_DIR, "config", "exercises_db.json")
ROOT_DIR = os.path.dirname(ENGINE_DIR)
STATE_FILE = os.path.join(ROOT_DIR, ".examshelp_state.json")

class StateManager:
    def __init__(self, workspace_subjects=None, workspace_rendu=None):
        if workspace_subjects is None:
            workspace_subjects = os.path.join(ROOT_DIR, "subjects")
        if workspace_rendu is None:
            workspace_rendu = os.path.join(ROOT_DIR, "rendu")
            
        self.workspace_subjects = workspace_subjects
        self.workspace_rendu = workspace_rendu
        self.session_mgr = SessionManager(
            history_dir=os.path.join(ROOT_DIR, "history"),
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
        return {"total_exercises": 118, "total_levels": 10, "levels": {str(i): [] for i in range(10)}}

    def _load_state(self):
        new_session_name = SessionManager.generate_cute_session_name()
        state = {
            "session_name": new_session_name,
            "current_level": 0,
            "active_exercise_id": None,
            "completed_exercises": [],
            "session_completed": [],
            "total_completions": 0,
            "language": "en",
            "history": []
        }
        
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
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
                            state["active_exercise_id"] = None
            except Exception:
                pass

        if "session_completed" not in state:
            state["session_completed"] = []
        if "total_completions" not in state:
            state["total_completions"] = len(state.get("completed_exercises", []))

        return state

    def reset_all_progress(self):
        """Resets all cumulative and per-session progress back to 0."""
        self.state["current_level"] = 0
        self.state["completed_exercises"] = []
        self.state["session_completed"] = []
        self.state["total_completions"] = 0
        self.state["active_exercise_id"] = None
        self.state["session_name"] = SessionManager.generate_cute_session_name()
        self.save_state()
        self.session_mgr.clean_workspace()
        self._select_random_exercise_for_level()
        self.save_state()
        self._sync_current_subject()

    def health_check(self):
        os.makedirs(self.workspace_subjects, exist_ok=True)
        os.makedirs(self.workspace_rendu, exist_ok=True)
        
        curr_lvl = self.state.get("current_level", 0)
        if not isinstance(curr_lvl, int) or curr_lvl < 0 or curr_lvl >= 10:
            self.state["current_level"] = 0
            
        active_ex = self.get_current_exercise()
        if not active_ex:
            self._select_random_exercise_for_level()
            
        self.save_state()
        self._sync_current_subject()

    def save_state(self):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def get_session_name(self):
        return self.state.get("session_name", "cute-session")

    def get_current_level(self):
        return self.state.get("current_level", 0)

    def get_current_exercise(self):
        lvl_str = str(self.get_current_level())
        level_exs = self.db.get("levels", {}).get(lvl_str, [])
        if not level_exs:
            return None
            
        active_id = self.state.get("active_exercise_id")
        if active_id:
            for ex in level_exs:
                if ex["id"] == active_id or ex["name"] == active_id:
                    return ex

        return self._select_random_exercise_for_level()

    def _select_random_exercise_for_level(self):
        lvl_str = str(self.get_current_level())
        level_exs = self.db.get("levels", {}).get(lvl_str, [])
        if not level_exs:
            return None
            
        completed = set(self.state.get("completed_exercises", []))
        uncompleted = [ex for ex in level_exs if ex["name"] not in completed]
        
        pool = uncompleted if uncompleted else level_exs
        chosen = random.choice(pool)
        self.state["active_exercise_id"] = chosen["id"]
        return chosen

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
        lvl = self.get_current_level()
        lvl_str = str(lvl)
        level_exs = self.db.get("levels", {}).get(lvl_str, [])
        completed = set(self.state.get("completed_exercises", []))
        
        uncompleted = [ex for ex in level_exs if ex["name"] not in completed]
        
        curr_id = self.state.get("active_exercise_id")
        different_candidates = [ex for ex in uncompleted if ex["id"] != curr_id and ex["name"] != curr_id]
        
        if different_candidates:
            chosen = random.choice(different_candidates)
            self.state["active_exercise_id"] = chosen["id"]
        elif uncompleted:
            chosen = random.choice(uncompleted)
            self.state["active_exercise_id"] = chosen["id"]
        else:
            if lvl + 1 < 10:
                self.state["current_level"] = lvl + 1
                self._select_random_exercise_for_level()
            else:
                if level_exs:
                    chosen = random.choice(level_exs)
                    self.state["active_exercise_id"] = chosen["id"]

        self.save_state()
        self._sync_current_subject()

    def archive_current_session(self, clean_workspace=True):
        current_name = self.get_session_name()
        folder, meta = self.session_mgr.archive_session(current_name, self.state)
        
        if clean_workspace:
            self.session_mgr.clean_workspace()
            
        self.state["session_archived"] = True
        self.state["session_name"] = SessionManager.generate_cute_session_name()
        self.state["session_completed"] = []
        self.state["active_exercise_id"] = None
        self.save_state()
        
        return folder, meta

    def _sync_current_subject(self):
        os.makedirs(self.workspace_subjects, exist_ok=True)
        ex = self.get_current_exercise()
        if ex:
            subj_content = ex.get("subject", f"Assignment name: {ex['name']}\nExpected files: {ex['expected_files']}\n")
            
            subj_path = os.path.join(self.workspace_subjects, f"subject_{ex['name']}.txt")
            with open(subj_path, "w", encoding="utf-8") as f:
                f.write(subj_content)
                
            active_subj_path = os.path.join(self.workspace_subjects, "subject.txt")
            with open(active_subj_path, "w", encoding="utf-8") as f:
                f.write(subj_content)

    def get_progress_data(self):
        total_completions = self.state.get("total_completions", 0)
        session_completed = len(self.state.get("session_completed", []))
        total = self.db.get("total_exercises", 118)
        curr_lvl = self.get_current_level()
        return {
            "session_name": self.get_session_name(),
            "current_level": curr_lvl,
            "session_completed_count": session_completed,
            "total_completions": total_completions,
            "total_count": total,
            "language": self.state.get("language", "en"),
            "current_exercise": self.get_current_exercise()
        }

    def set_language(self, lang):
        self.state["language"] = lang
        self.save_state()
