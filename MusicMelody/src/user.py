import json
import os
from datetime import datetime


class User:
    def __init__(self, username):
        self.username = username
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.history_file = os.path.join(self.base_dir, "data", "history.json")
        self._ensure_file()
        self.history = self._load_history()

    def _ensure_file(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({}, f)

    def _load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return data.get(self.username, [])
        except:
            return []

    def log_song(self, song):
        # Generate the EXACT current time
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = {
            "title": song['title'],
            "artist": song['artist'],
            "timestamp": now_str
        }

        self.history.insert(0, entry)

        self._save_to_file()
    def _save_to_file(self):
        try:
            existing_data = {}
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            existing_data[self.username] = self.history
            with open(self.history_file, 'w') as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            print(f"History Save Error: {e}")
