import webbrowser
import json
import os
from youtubesearchpython import VideosSearch


class MusicRecommender:
    def __init__(self):
        # Week 3 Requirement: Store Data
        self.db_file = "music_db.json"
        self.db = self._load_db()

    def _load_db(self):
        """Loads the database from a JSON file into a Python Dictionary"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}  # Return empty dict if file doesn't exist

    def _save_db(self):
        """Saves the current dictionary to the JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.db, f, indent=4)

    def get_recommendations(self, mood):
        # 1. CHECK DATABASE FIRST
        if mood in self.db and self.db[mood]:
            print(f"DEBUG: Found {mood} songs in local database.")
            return self.db[mood]

        # 2. IF NOT IN DB, SEARCH YOUTUBE
        print(f"DEBUG: {mood} not in DB. Searching YouTube...")
        query = f"best {mood} music playlist"
        videosSearch = VideosSearch(query, limit=5)
        results = videosSearch.result()

        song_list = []
        if 'result' in results:
            for video in results['result']:
                song_list.append({
                    'title': video['title'],
                    'link': video['link'],
                    'duration': video.get('duration', 'N/A')
                })

        # 3. SAVE NEW RESULTS TO DATABASE
        self.db[mood] = song_list
        self._save_db()

        return song_list

    def play_music(self, url):
        webbrowser.open(url)
