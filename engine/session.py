import os
import random
import json
import shutil
import datetime

ADJECTIVES = [
    "happy", "sleepy", "brave", "clever", "sunny", "cozy", "fuzzy", "swift",
    "gentle", "mighty", "cosmic", "golden", "noble", "dancing", "whistling",
    "sparkling", "velvet", "nimble", "playful", "bubbly"
]

ANIMALS = [
    "sparrow", "panda", "otter", "fox", "koala", "penguin", "cat", "rabbit",
    "owl", "dolphin", "bear", "badger", "lynx", "falcon", "robin", "beaver",
    "squirrel", "hedgehog", "capybara", "raccoon"
]

SNACKS = [
    "banana", "cookie", "mango", "coffee", "donut", "waffle", "berry",
    "pretzel", "biscuit", "muffin", "matcha", "hazelnut", "marshmallow",
    "pancake", "chocolat", "tapioca", "cupcake", "macaron", "caramel", "croissant"
]

class SessionManager:
    def __init__(self, history_dir="history", rendu_dir="rendu", subjects_dir="subjects"):
        self.history_dir = history_dir
        self.rendu_dir = rendu_dir
        self.subjects_dir = subjects_dir
        os.makedirs(self.history_dir, exist_ok=True)

    @staticmethod
    def generate_cute_session_name():
        adj = random.choice(ADJECTIVES)
        animal = random.choice(ANIMALS)
        snack = random.choice(SNACKS)
        return f"{adj}-{animal}-{snack}"

    def archive_session(self, session_name, state_data):
        """
        Archives current session's rendu code, subjects, and progress into history/<session_name>/.
        """
        if not session_name:
            session_name = self.generate_cute_session_name()
            
        session_folder = os.path.join(self.history_dir, session_name)
        os.makedirs(session_folder, exist_ok=True)
        
        # 1. Archive rendu/ C code
        archived_rendu = os.path.join(session_folder, "rendu")
        os.makedirs(archived_rendu, exist_ok=True)
        if os.path.exists(self.rendu_dir):
            for item in os.listdir(self.rendu_dir):
                s_path = os.path.join(self.rendu_dir, item)
                d_path = os.path.join(archived_rendu, item)
                if os.path.isdir(s_path):
                    shutil.copytree(s_path, d_path, dirs_exist_ok=True)
                elif os.path.isfile(s_path):
                    shutil.copy2(s_path, d_path)

        # 2. Archive subjects/
        archived_subjects = os.path.join(session_folder, "subjects")
        os.makedirs(archived_subjects, exist_ok=True)
        if os.path.exists(self.subjects_dir):
            for item in os.listdir(self.subjects_dir):
                s_path = os.path.join(self.subjects_dir, item)
                d_path = os.path.join(archived_subjects, item)
                if os.path.isdir(s_path):
                    shutil.copytree(s_path, d_path, dirs_exist_ok=True)
                elif os.path.isfile(s_path):
                    shutil.copy2(s_path, d_path)

        # 3. Save session metadata
        track = state_data.get("current_track", "")
        track_progress = state_data.get("progress", {}).get(track) or {}
        meta = {
            "session_name": session_name,
            "archived_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_track": track,
            # Kept under the old key so archives from before exams existed still
            # list correctly; it now means "level within current_track".
            "current_level": track_progress.get("level", 0),
            "completed_exercises": state_data.get("completed_exercises", []),
            "completed_count": len(state_data.get("completed_exercises", [])),
            "archived_rendu_files": os.listdir(archived_rendu) if os.path.exists(archived_rendu) else []
        }
        
        meta_path = os.path.join(session_folder, "session_info.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
            
        return session_folder, meta

    def clean_workspace(self):
        """
        Cleans up rendu/ and subjects/ workspace upon exit so it is fresh for next session.
        All C code and subjects are preserved safely in history/<session_name>/.
        """
        if os.path.exists(self.rendu_dir):
            for item in os.listdir(self.rendu_dir):
                p = os.path.join(self.rendu_dir, item)
                try:
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                except Exception:
                    pass

        if os.path.exists(self.subjects_dir):
            for item in os.listdir(self.subjects_dir):
                p = os.path.join(self.subjects_dir, item)
                try:
                    if os.path.isdir(p):
                        shutil.rmtree(p)
                    else:
                        os.remove(p)
                except Exception:
                    pass

    def list_saved_sessions(self):
        sessions = []
        if not os.path.exists(self.history_dir):
            return sessions
            
        for item in os.listdir(self.history_dir):
            folder = os.path.join(self.history_dir, item)
            info_file = os.path.join(folder, "session_info.json")
            if os.path.isdir(folder) and os.path.exists(info_file):
                try:
                    with open(info_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        sessions.append(meta)
                except Exception:
                    pass
                    
        sessions.sort(key=lambda x: x.get("archived_at", ""), reverse=True)
        return sessions
