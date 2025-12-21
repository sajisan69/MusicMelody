import tkinter as tk
from tkinter import messagebox, ttk

class UIHandler:
    def __init__(self, root, user, mood_analyzer, recommender):
        self.user = user
        self.mood_analyzer = mood_analyzer
        self.recommender = recommender

        self.root = root
        self.root.title("🎵 Music Melody - Mood Based Music Recommender")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # ---------- Style ----------
        self.root.configure(bg="#1e1e2f")
        self.font_large = ("Helvetica", 14, "bold")
        self.font_medium = ("Helvetica", 12)
        self.fg_color = "#ffffff"
        self.bg_color = "#1e1e2f"

        # ---------- Header ----------
        self.header = tk.Label(root, text=f"Welcome {self.user.get_username()}!", font=("Helvetica", 18, "bold"),
                               bg=self.bg_color, fg="#ffdd57")
        self.header.pack(pady=15)

        # ---------- Mood Input ----------
        self.label_mood = tk.Label(root, text="How are you feeling today?", font=self.font_medium,
                                   bg=self.bg_color, fg=self.fg_color)
        self.label_mood.pack(pady=5)

        self.entry_mood = tk.Entry(root, width=30, font=self.font_medium)
        self.entry_mood.pack(pady=5)

        # ---------- Button ----------
        self.btn_recommend = tk.Button(root, text="Get Music Recommendations", font=self.font_medium,
                                       bg="#ff6b6b", fg="white", command=self.show_recommendations)
        self.btn_recommend.pack(pady=15)

        # ---------- Output Box ----------
        self.output_box = tk.Text(root, width=55, height=10, font=self.font_medium, bg="#2e2e3e", fg=self.fg_color)
        self.output_box.pack(pady=10)
        self.output_box.config(state='disabled')

        # ---------- Separator ----------
        self.separator = ttk.Separator(root, orient='horizontal')
        self.separator.pack(fill='x', pady=10)

        # ---------- Footer ----------
        self.footer = tk.Label(root, text="Music Melody © 2025", font=("Helvetica", 10), bg=self.bg_color, fg="#aaaaaa")
        self.footer.pack(side='bottom', pady=5)

    def show_recommendations(self):
        mood_text = self.entry_mood.get().strip()
        if not mood_text:
            messagebox.showwarning("Input Error", "Please enter your mood!")
            return

        mood = self.mood_analyzer.analyze_mood(mood_text)
        recommendations = self.recommender.recommend_music(mood)

        # Show in output box
        self.output_box.config(state='normal')
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"Detected Mood: {mood}\n\nRecommended Songs:\n")
        for song in recommendations:
            self.output_box.insert(tk.END, f"- {song}\n")
        self.output_box.config(state='disabled')
