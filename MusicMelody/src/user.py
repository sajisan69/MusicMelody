class User:
    def __init__(self, username):
        self.username = username
        self.mood_history = []

    def add_mood_to_history(self, mood):
        """Adds a mood to the history list."""
        if mood and mood != "Neutral":
            self.mood_history.append(mood)
            # Keep only last 20 entries to save memory
            if len(self.mood_history) > 20:
                self.mood_history.pop(0)

    def get_history(self):
        return self.mood_history
