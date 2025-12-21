import json
import os

class MusicRecommender:
    def __init__(self, json_file="data/music_library.json"):
        # Get absolute path
        abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), json_file)
        try:
            with open(abs_path, "r") as f:
                self.__music_library = json.load(f)
        except FileNotFoundError:
            self.__music_library = {
                "happy": ["Happy by Pharrell", "Can't Stop the Feeling by Justin"],
                "sad": ["Someone Like You by Adele", "Fix You by Coldplay"],
                "angry": ["Break Stuff by Limp Bizkit", "Killing In The Name by Rage Against the Machine"],
                "neutral": ["Shape of You by Ed Sheeran", "Blinding Lights by The Weeknd"]
            }

    def recommend_music(self, mood):
        return self.__music_library.get(mood, self.__music_library["neutral"])
