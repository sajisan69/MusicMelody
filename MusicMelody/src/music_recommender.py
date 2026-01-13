import json
import os
import pygame


class MusicRecommender:
    def __init__(self):
        # 1. Setup Paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.base_dir, "data", "music_db.json")
        self.songs_dir = os.path.join(self.base_dir, "songs")

        # 2. Initialize Mixer
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Audio Error: {e}")

        self.songs_data = self._load_data()
        self.current_song_file = None
        self.is_paused = False
        self.start_offset = 0.0

    def _load_data(self):
        if not os.path.exists(self.db_path):
            return {}
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return {}

    def get_recommendations(self, mood):
        return self.songs_data.get(mood, [])

    # --- SMART TOGGLE ---
    def toggle_pause(self):
        """Toggles between Play and Pause. Returns the new state string."""
        if not self.current_song_file:
            return "stopped"

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            return "playing"
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            return "paused"

    # --- PLAYER CONTROLS ---
    def play_song(self, filename, start_time=0.0):
        path = os.path.join(self.songs_dir, filename)

        if not os.path.exists(path):
            print(f"File missing: {path}")
            return False

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(start=start_time)
            self.current_song_file = filename
            self.start_offset = start_time
            self.is_paused = False
            return True
        except Exception as e:
            print(f"Playback Error: {e}")
            return False

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.current_song_file = None
        self.start_offset = 0.0

    def set_volume(self, val):
        try:
            pygame.mixer.music.set_volume(float(val))
        except:
            pass

    def seek(self, seconds):
        if not self.current_song_file: return
        current_pos_ms = pygame.mixer.music.get_pos()
        if current_pos_ms == -1: return

        current_pos_sec = (current_pos_ms / 1000) + self.start_offset
        new_pos = max(0, current_pos_sec + seconds)
        self.play_song(self.current_song_file, start_time=new_pos)
