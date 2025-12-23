import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
import threading
import time

# --- IMPORTS ---
from src.user import User
from src.mood_analyzer import MoodAnalyzer
from src.music_recommender import MusicRecommender


class UIHandler:
    def __init__(self):
        # --- FLAGSHIP COLOR PALETTE ---
        self.colors = {
            "sidebar": "#121212",  # Spotify-like Black
            "main_bg": "#181818",  # Dark Grey
            "card_bg": "#282828",  # Lighter Grey for cards
            "accent": "#1DB954",  # Professional Green
            "text_main": "#FFFFFF",  # White
            "text_sub": "#B3B3B3",  # Light Grey
            "hover": "#3E3E3E"  # Hover state
        }

        # Logic
        self.user = User()
        self.analyzer = MoodAnalyzer()
        self.recommender = MusicRecommender()

        # Window Setup
        self.root = tk.Tk()
        self.root.title("MusicMelody | Pro Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.colors["main_bg"])

        # Custom Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", foreground=self.colors['accent'],
                        background=self.colors['accent'])

        # Fonts
        self.f_head = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.f_sub = tkfont.Font(family="Segoe UI", size=10)
        self.f_bold = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        # Grid Layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._build_layout()

    def _build_layout(self):
        # 1. SIDEBAR
        sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🎵 MusicMelody", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["sidebar"], fg="white").pack(pady=(30, 40))

        self._sidebar_item(sidebar, "🏠  Home", active=True)
        self._sidebar_item(sidebar, "🔍  Search")
        self._sidebar_item(sidebar, "📚  Your Library")

        tk.Frame(sidebar, bg=self.colors["card_bg"], height=1).pack(fill="x", padx=20, pady=20)

        tk.Label(sidebar, text="PLAYLISTS", font=("Segoe UI", 8, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["text_sub"]).pack(anchor="w", padx=25)

        self._sidebar_item(sidebar, "❤️  Liked Songs")

        # 2. MAIN CONTENT
        main = tk.Frame(self.root, bg=self.colors["main_bg"], padx=40, pady=30)
        main.grid(row=0, column=1, sticky="nsew")

        tk.Label(main, text="Good evening,", font=self.f_head, bg=self.colors["main_bg"], fg="white").pack(anchor="w")
        tk.Label(main, text="What's on your mind?", font=self.f_sub, bg=self.colors["main_bg"],
                 fg=self.colors["text_sub"]).pack(anchor="w", pady=(0, 20))

        # Search Bar
        search_frame = tk.Frame(main, bg=self.colors["card_bg"], pady=2, padx=2)
        search_frame.pack(fill="x", pady=(0, 20))

        self.entry = tk.Entry(search_frame, font=("Segoe UI", 12), bg=self.colors["card_bg"],
                              fg="white", insertbackground="white", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, padx=10, ipady=8)
        self.entry.bind('<Return>', lambda e: self._on_analyze())

        btn = tk.Button(search_frame, text="FIND VIBE", bg=self.colors["accent"], fg="white",
                        font=self.f_bold, relief="flat", cursor="hand2", command=self._on_analyze)
        btn.pack(side="right", padx=5, fill="y")

        # Mood & Progress
        self.info_frame = tk.Frame(main, bg=self.colors["main_bg"])
        self.info_frame.pack(fill="x", pady=10)

        self.lbl_mood = tk.Label(self.info_frame, text="", font=("Segoe UI", 12), bg=self.colors["main_bg"],
                                 fg=self.colors["accent"])
        self.lbl_mood.pack(anchor="w")

        self.progress = ttk.Progressbar(self.info_frame, style="green.Horizontal.TProgressbar", orient="horizontal",
                                        length=200, mode="indeterminate")

        # Results List
        tk.Label(main, text="Recommended for you", font=("Segoe UI", 11, "bold"),
                 bg=self.colors["main_bg"], fg="white").pack(anchor="w", pady=(20, 10))

        self.results_container = tk.Frame(main, bg=self.colors["main_bg"])
        self.results_container.pack(fill="both", expand=True)

        # 3. PLAYER FOOTER (Visual Only)
        footer = tk.Frame(self.root, bg="#181818", height=90, highlightbackground="#282828", highlightthickness=1)
        footer.grid(row=1, column=0, columnspan=2, sticky="ew")
        footer.pack_propagate(False)

        self.lbl_now_playing = tk.Label(footer, text="MusicMelody AI", font=("Segoe UI", 10, "bold"), bg="#181818",
                                        fg="white")
        self.lbl_now_playing.place(x=20, y=25)
        self.lbl_artist = tk.Label(footer, text="Select a song to view...", font=("Segoe UI", 8), bg="#181818",
                                   fg="#B3B3B3")
        self.lbl_artist.place(x=20, y=45)

        tk.Label(footer, text="⏮   ⏯   ⏭", font=("Segoe UI", 16), bg="#181818", fg="white").place(relx=0.5, rely=0.4,
                                                                                                  anchor="center")
        tk.Label(footer, text="0:00 ──────────●───────── 3:45", font=("Segoe UI", 8), bg="#181818", fg="#B3B3B3").place(
            relx=0.5, rely=0.7, anchor="center")

    def _sidebar_item(self, parent, text, active=False):
        fg = "white" if active else self.colors["text_sub"]
        lbl = tk.Label(parent, text=text, font=self.f_bold if active else self.f_sub,
                       bg=self.colors["sidebar"], fg=fg, cursor="hand2")
        lbl.pack(anchor="w", padx=25, pady=10)
        lbl.bind("<Enter>", lambda e: lbl.config(fg="white"))
        lbl.bind("<Leave>", lambda e: lbl.config(fg=fg))

    def _on_analyze(self):
        text = self.entry.get()
        if not text.strip(): return

        for widget in self.results_container.winfo_children(): widget.destroy()
        self.lbl_mood.config(text="Analyzing text patterns...")
        self.progress.pack(anchor="w", pady=5, fill="x")
        self.progress.start(10)

        self.user.set_mood_text(text)
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _process(self, text):
        mood, emoji = self.analyzer.get_mood_category(text)
        time.sleep(0.8)

        self.root.after(0, lambda: self.lbl_mood.config(text=f"{emoji} Mood Detected: {mood}"))

        # NOTE: Music is still STORED here by get_recommendations
        songs = self.recommender.get_recommendations(mood)

        self.root.after(0, self.progress.stop)
        self.root.after(0, self.progress.pack_forget)
        self.root.after(0, lambda: self._show_results(songs))

    def _show_results(self, songs):
        if not songs:
            tk.Label(self.results_container, text="No songs found.", bg=self.colors["main_bg"], fg="red").pack()
            return

        for i, song in enumerate(songs):
            self._draw_song_row(song, i + 1)

    def _draw_song_row(self, song, num):
        row = tk.Frame(self.results_container, bg=self.colors["main_bg"], pady=8)
        row.pack(fill="x")

        tk.Label(row, text=str(num), width=4, bg=self.colors["main_bg"], fg=self.colors["text_sub"]).pack(side="left")

        tk.Frame(row, bg="#333", width=35, height=35).pack(side="left", padx=10)

        info = tk.Frame(row, bg=self.colors["main_bg"])
        info.pack(side="left", fill="x", expand=True)

        title = song['title']
        if len(title) > 50: title = title[:47] + "..."

        tk.Label(info, text=title, font=self.f_bold, bg=self.colors["main_bg"], fg="white", anchor="w").pack(fill="x")
        tk.Label(info, text="YouTube Music", font=("Segoe UI", 8), bg=self.colors["main_bg"],
                 fg=self.colors["text_sub"], anchor="w").pack(fill="x")

        tk.Label(row, text=song['duration'], bg=self.colors["main_bg"], fg=self.colors["text_sub"], padx=15).pack(
            side="right")

        # --- PLAY BUTTON (Select Only) ---
        btn = tk.Button(row, text="▶", bg=self.colors["main_bg"], fg="white", bd=0,
                        font=("Arial", 14), cursor="hand2", activebackground=self.colors["main_bg"],
                        # This calls _select_song, NOT web browser
                        command=lambda t=song['title']: self._select_song(t))
        btn.pack(side="right", padx=10)

        row.bind("<Enter>", lambda e: row.config(bg=self.colors["card_bg"]))
        row.bind("<Leave>", lambda e: row.config(bg=self.colors["main_bg"]))

    def _select_song(self, title):
        """
        UPDATED: Updates the UI to show the song is selected,
        but DOES NOT open the web browser.
        """
        # 1. Update the footer text
        self.lbl_now_playing.config(text=title[:30] + "..." if len(title) > 30 else title)
        self.lbl_artist.config(text="Selected (Ready to Play)")

        # 2. No webbrowser.open() here!
        print(f"User selected: {title}")

    # --- THIS WAS MISSING ---
    def run(self):
        self.root.mainloop()
