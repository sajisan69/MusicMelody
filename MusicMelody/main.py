import tkinter as tk
from src.user import User
from src.mood_analyzer import MoodAnalyzer
from src.music_recommender import MusicRecommender
from src.ui_handler import UIHandler

def main():
    # Initialize classes
    user = User("Jisan", age=20, favorite_genres=["pop", "rock"])
    mood_analyzer = MoodAnalyzer()
    recommender = MusicRecommender()

    # Tkinter root
    root = tk.Tk()
    app = UIHandler(root, user, mood_analyzer, recommender)
    root.mainloop()

if __name__ == "__main__":
    main()
