class MoodAnalyzer:
    def __init__(self):
        self.keywords = {
            "Happy": ["happy", "joy", "excited", "good", "great", "awesome", "fun", "glad", "smile", "laugh"],
            "Sad": ["sad", "cry", "depressed", "blue", "bad", "lonely", "down", "upset", "hurt", "pain", "grief"],
            "Energetic": ["energy", "run", "gym", "party", "dance", "active", "power", "workout", "jump", "fast"],
            "Calm": ["sleep", "relax", "calm", "peace", "quiet", "nap", "meditate", "yoga", "rest", "zen"],
            "Angry": ["angry", "mad", "furious", "hate", "rage", "annoyed", "irritated", "scream", "fight"],
            "Focused": ["focus", "work", "coding", "code", "study", "concentration", "learn", "read", "busy", "task"],
            "Romantic": ["love", "date", "romantic", "crush", "heart", "beautiful", "sweet", "kiss", "couple", "marry"],
            "Chill": ["chill", "vibe", "cool", "drive", "smoke", "easy", "slow", "lazy", "bored", "hangout"],
            "Motivated": ["win", "success", "goal", "dream", "achieve", "hustle", "grind", "inspire", "ambition"]
        }
    def analyze_mood(self, text):
        text = text.lower()
        for mood, words in self.keywords.items():
            if any(word in text for word in words):
                return mood
        return "Neutral"
