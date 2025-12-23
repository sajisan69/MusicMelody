from textblob import TextBlob


class MoodAnalyzer:
    def __init__(self):
        # Data Structure: Dictionary for exact keyword matching
        self.keyword_map = {
            "happy": "Happy", "joy": "Happy", "good": "Happy",
            "sad": "Melancholic", "cry": "Melancholic", "bad": "Melancholic",
            "angry": "Energetic", "party": "Energetic", "gym": "Energetic",
            "sleep": "Calm", "tired": "Calm", "relax": "Calm",
            "study": "Deep Focus", "work": "Deep Focus", "focus": "Deep Focus"
        }

    def get_mood_category(self, text):
        """
        Logic: Check keywords first -> Fallback to AI (TextBlob)
        Returns: (Mood Name, Emoji)
        """
        text_lower = text.lower()

        # 1. KEYWORD DETECTION (Week 3 Requirement)
        for word, mood in self.keyword_map.items():
            if word in text_lower:
                return mood, self._get_emoji(mood)

        # 2. SENTIMENT ANALYSIS (Fallback)
        blob = TextBlob(text)
        score = blob.sentiment.polarity

        if score > 0.5:
            return "Energetic", "🔥"
        elif 0 < score <= 0.5:
            return "Happy", "😊"
        elif -0.5 <= score < 0:
            return "Melancholic", "🌧️"
        elif score < -0.5:
            return "Deep Focus", "🧘"
        else:
            return "Calm", "☕"

    def _get_emoji(self, mood):
        # Helper to get emoji for keywords
        emojis = {
            "Happy": "😊", "Melancholic": "🌧️",
            "Energetic": "🔥", "Calm": "☕", "Deep Focus": "🧘"
        }
        return emojis.get(mood, "🎵")
