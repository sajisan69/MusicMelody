import string

class MoodAnalyzer:
    def __init__(self):
        self.__mood = None

    def analyze_mood(self, mood_text):
        # Clean input
        mood_text = mood_text.lower().strip()
        mood_text = mood_text.translate(str.maketrans('', '', string.punctuation))

        happy_keywords = ["happy", "joy", "awesome", "great", "excited", "😊", "😁"]
        sad_keywords = ["sad", "down", "unhappy", "depressed", "😢", "😭"]
        angry_keywords = ["angry", "mad", "frustrated", "😡", "😠"]

        # Check keywords anywhere in the text
        if any(word in mood_text for word in happy_keywords):
            self.__mood = "happy"
        elif any(word in mood_text for word in sad_keywords):
            self.__mood = "sad"
        elif any(word in mood_text for word in angry_keywords):
            self.__mood = "angry"
        else:
            self.__mood = "neutral"

        return self.__mood

    def get_mood(self):
        return self.__mood
