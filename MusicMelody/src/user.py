class User:
    # 1. We added '="Guest"' so you can create a user without providing a name immediately.
    def __init__(self, username="Guest", age=None, favorite_genres=None):
        self.__username = username
        self.__age = age
        self.__favorite_genres = favorite_genres if favorite_genres else []

        # 2. We added this to store the mood (Required by UIHandler)
        self._current_mood_text = ""

    def get_username(self):
        return self.__username

    def get_age(self):
        return self.__age

    def get_favorite_genres(self):
        return self.__favorite_genres

    def add_genre(self, genre):
        if genre not in self.__favorite_genres:
            self.__favorite_genres.append(genre)

    # 3. These methods were missing! The UI needs them to save your input.
    def set_mood_text(self, text):
        self._current_mood_text = text

    def get_mood_text(self):
        return self._current_mood_text
