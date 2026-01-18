import pygame
import os
import shutil
import json
import random


class MusicRecommender:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        except pygame.error as e:
            print(f"Audio Device Error: {e}")

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.songs_dir = os.path.join(self.base_dir, "songs")
        self.db_file = os.path.join(self.base_dir, "data", "music_db.json")

        if not os.path.exists(self.songs_dir): os.makedirs(self.songs_dir)
        self.music_db = self._load_db()
        self.current_song_path = None
        self.is_paused = False

    def _load_db(self):
        if not os.path.exists(self.db_file): return {}
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_db(self):
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.music_db, f, indent=4)
        except Exception as e:
            print(f"DB Save Error: {e}")

    def get_all_songs(self):
        all_songs = []
        for mood, songs in self.music_db.items():
            all_songs.extend(songs)
        random.shuffle(all_songs)
        return all_songs

    def get_user_uploads(self, username):
        user_songs = []
        for mood, songs in self.music_db.items():
            for song in songs:
                # Check if 'uploaded_by' exists and matches
                if song.get('uploaded_by') == username:
                    user_songs.append(song)
        return user_songs

    def get_recommendations(self, mood):
        mood_key = mood.capitalize()
        if mood_key in self.music_db: return self.music_db[mood_key]
        for key in self.music_db:
            if mood.lower() in key.lower(): return self.music_db[key]
        return []

    def play_song(self, filename):
        path = os.path.join(self.songs_dir, filename)
        if not os.path.exists(path): return False, "File not found"
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.current_song_path = path
            self.is_paused = False
            return True, "Playing"
        except Exception as e:
            return False, str(e)

    def stop_song(self):
        pygame.mixer.music.stop()

    def toggle_pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause();
            self.is_paused = False;
            return "playing"
        else:
            pygame.mixer.music.pause();
            self.is_paused = True;
            return "paused"

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def seek_song(self, seconds):
        try:
            current = pygame.mixer.music.get_pos()
            target = (current / 1000) + seconds
            pygame.mixer.music.set_pos(max(0, target))
        except:
            pass

    def add_song(self, title, artist, mood, file_path, username):
        filename = os.path.basename(file_path)
        dest = os.path.join(self.songs_dir, filename)
        try:
            shutil.copy(file_path, dest)
            new_song = {
                "title": title,
                "artist": artist,
                "filename": filename,
                "uploaded_by": username
            }
            mood_key = mood.capitalize()
            if mood_key in self.music_db:
                self.music_db[mood_key].append(new_song)
            else:
                self.music_db[mood_key] = [new_song]
            self._save_db()
            return True, "Song added!"
        except Exception as e:
            return False, str(e)
