class User:
    def __init__(self, username, age=None, favorite_genres=None):
        self.__username = username
        self.__age = age
        self.__favorite_genres = favorite_genres if favorite_genres else []

    def get_username(self):
        return self.__username

    def get_age(self):
        return self.__age

    def get_favorite_genres(self):
        return self.__favorite_genres

    def add_genre(self, genre):
        if genre not in self.__favorite_genres:
            self.__favorite_genres.append(genre)
