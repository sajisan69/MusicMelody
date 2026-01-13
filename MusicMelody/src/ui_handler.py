import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, Canvas, Scale
import random

from src.user import User
from src.mood_analyzer import MoodAnalyzer
from src.music_recommender import MusicRecommender


class UIHandler:
    def __init__(self):
        # --- NEW "DEEP SPACE" COLOR PALETTE (NO BLACK) ---
        self.colors = {
            "bg": "#1E1E2E",  # Deep Blue-Grey (Not Black)
            "sidebar": "#181825",  # Darker Blue-Grey for sidebar
            "card_bg": "#313244",  # Soft Slate for cards
            "card_hover": "#45475A",  # Lighter Slate for hover
            "accent_1": "#89B4FA",  # Soft Blue
            "accent_2": "#F38BA8",  # Soft Red/Pink
            "text_main": "#CDD6F4",  # White-ish
            "text_sub": "#A6ADC8",  # Grey-ish
            "player_bg": "#11111B"  # Very dark blue for player
        }

        self.quotes = [
            "\"Music is the strongest form of magic.\"",
            "\"Where words leave off, music begins.\"",
            "\"Life involves rhythm, accept it.\"",
            "\"Music washes away from the soul the dust of everyday life.\""
        ]

        # Backend
        self.user = User("MusicLover")
        self.analyzer = MoodAnalyzer()
        self.recommender = MusicRecommender()

        # --- STATE MEMORY (Fixes the erasing issue) ---
        self.last_mood = None
        self.last_songs = []
        self.player_visible = False

        # Window Setup
        self.root = tk.Tk()
        self.root.title("MusicMelody | Modern Blue")
        self.root.geometry("1150x780")
        self.root.configure(bg=self.colors["bg"])

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._init_ui()

    def _init_ui(self):
        # 1. SIDEBAR
        sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=260)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
        sidebar.pack_propagate(False)

        # Logo
        tk.Label(sidebar, text="🎵 MusicMelody", font=("Segoe UI", 18, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["accent_1"]).pack(pady=(50, 5))

        tk.Label(sidebar, text="MODERN BLUE", font=("Segoe UI", 8, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["accent_2"]).pack(pady=(0, 50))

        # Nav Buttons
        self._nav_btn(sidebar, "🏠  HOME", self._show_home)
        self._nav_btn(sidebar, "📜  HISTORY", self._show_history)

        # 2. MAIN AREA
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"], padx=60, pady=40)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # 3. HIDDEN PLAYER BAR
        self.player_frame = tk.Frame(self.root, bg=self.colors["player_bg"], height=110,
                                     highlightbackground=self.colors["card_bg"], highlightthickness=1)

        self._show_home()

    def _nav_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"],
                        fg=self.colors["text_sub"], bd=0, anchor="w", cursor="hand2", command=cmd, padx=40, pady=12,
                        activebackground=self.colors["bg"], activeforeground=self.colors["accent_1"])
        btn.pack(fill="x", pady=2)

    # --- PLAYER BAR ---
    def _build_player_ui(self):
        for widget in self.player_frame.winfo_children(): widget.destroy()

        # Art & Info
        art_box = tk.Frame(self.player_frame, bg=self.colors["player_bg"], width=300)
        art_box.pack(side="left", fill="y", padx=20, pady=15)

        art_sq = tk.Frame(art_box, bg=self.colors["accent_2"], width=70, height=70)
        art_sq.pack(side="left")
        art_sq.pack_propagate(False)
        tk.Label(art_sq, text="♫", font=("Arial", 24), bg=self.colors["accent_2"], fg=self.colors["player_bg"]).pack(
            expand=True)

        info = tk.Frame(art_box, bg=self.colors["player_bg"])
        info.pack(side="left", padx=15)

        self.lbl_title = tk.Label(info, text="Song Title", font=("Segoe UI", 12, "bold"),
                                  bg=self.colors["player_bg"], fg="white", anchor="w")
        self.lbl_title.pack(anchor="w")

        self.lbl_artist = tk.Label(info, text="Artist", font=("Segoe UI", 10),
                                   bg=self.colors["player_bg"], fg=self.colors["text_sub"], anchor="w")
        self.lbl_artist.pack(anchor="w")

        # Controls
        controls = tk.Frame(self.player_frame, bg=self.colors["player_bg"])
        controls.pack(side="left", expand=True)

        self._control_btn(controls, "⏪", lambda: self.recommender.seek(-10), 14)
        self._control_btn(controls, "⏹", self._stop_ui, 16, color=self.colors["accent_2"])

        self.btn_play = tk.Button(controls, text="⏸", command=self._toggle_play_pause,
                                  bg=self.colors["accent_1"], fg=self.colors["player_bg"], bd=0, font=("Segoe UI", 18),
                                  width=4, height=1, cursor="hand2")
        self.btn_play.pack(side="left", padx=20)

        self._control_btn(controls, "⏩", lambda: self.recommender.seek(10), 14)

        # Volume
        vol_frame = tk.Frame(self.player_frame, bg=self.colors["player_bg"])
        vol_frame.pack(side="right", padx=40)
        tk.Label(vol_frame, text="🔊", bg=self.colors["player_bg"], fg=self.colors["text_sub"]).pack(side="left", padx=5)

        scale = Scale(vol_frame, from_=0, to=1, resolution=0.1, orient="horizontal",
                      bg=self.colors["player_bg"], fg=self.colors["accent_1"], highlightthickness=0,
                      length=100, showvalue=0, troughcolor=self.colors["card_bg"], command=self.recommender.set_volume)
        scale.set(0.5)
        scale.pack(side="left")

    def _control_btn(self, parent, text, cmd, size, color=None):
        if color is None: color = self.colors["text_main"]
        btn = tk.Button(parent, text=text, command=cmd, bg=self.colors["player_bg"], fg=color,
                        bd=0, font=("Segoe UI", size), cursor="hand2", activebackground=self.colors["player_bg"])
        btn.pack(side="left", padx=15)

    # --- HOME LOGIC ---
    def _show_home(self):
        self._clear_main()

        # Header
        quote = random.choice(self.quotes)
        tk.Label(self.main_area, text=quote, font=("Georgia", 16, "italic"),
                 bg=self.colors["bg"], fg=self.colors["text_sub"]).pack(anchor="w", pady=(0, 10))

        tk.Label(self.main_area, text="What do you want to hear?", font=("Segoe UI", 12, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text_main"]).pack(anchor="w", pady=(0, 25))

        # Search Bar
        input_frame = tk.Frame(self.main_area, bg=self.colors["bg"])
        input_frame.pack(fill="x", pady=(0, 30))

        self.entry = tk.Entry(input_frame, font=("Segoe UI", 16), bg=self.colors["card_bg"],
                              fg=self.colors["text_main"], relief="flat", insertbackground="white")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 15))

        btn_go = tk.Button(input_frame, text="SEARCH VIBE", bg=self.colors["accent_1"], fg=self.colors["player_bg"],
                           font=("Segoe UI", 11, "bold"), command=self._detect_mood,
                           padx=25, pady=8, bd=0, cursor="hand2")
        btn_go.pack(side="right")

        # --- RESTORE PREVIOUS SEARCH (Fixes Erasing) ---
        self._setup_scroll_area()

        if self.last_songs:
            self._render_results(self.last_mood, self.last_songs)
        else:
            tk.Label(self.scrollable_frame, text="Try searching for 'Happy', 'Sad', or 'Focused'...",
                     bg=self.colors["bg"], fg=self.colors["text_sub"], font=("Segoe UI", 12)).pack(pady=20)

    def _setup_scroll_area(self):
        container = tk.Frame(self.main_area, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        self.canvas = Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=container.winfo_width())

        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas.find_all()[0], width=e.width))

        self.canvas.pack(side="left", fill="both", expand=True)

    def _detect_mood(self):
        text = self.entry.get()
        if not text: return

        mood = self.analyzer.analyze_mood(text)
        self.user.add_mood_to_history(mood)
        songs = self.recommender.get_recommendations(mood)

        # SAVE STATE
        self.last_mood = mood
        self.last_songs = songs

        self._render_results(mood, songs)

    def _render_results(self, mood, songs):
        # Clear previous list
        for w in self.scrollable_frame.winfo_children(): w.destroy()

        # Mood Title
        tk.Label(self.scrollable_frame, text=f"Mood: {mood}", font=("Segoe UI", 20, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent_1"]).pack(anchor="w", pady=(10, 5))

        if not songs:
            tk.Label(self.scrollable_frame, text="No songs found.", bg=self.colors["bg"],
                     fg=self.colors["accent_2"]).pack()

        for song in songs:
            self._create_interactive_row(song)

    def _create_interactive_row(self, song):
        card = tk.Frame(self.scrollable_frame, bg=self.colors["card_bg"], pady=15, padx=20, cursor="hand2")
        card.pack(fill="x", pady=5)

        title = tk.Label(card, text=song['title'], font=("Segoe UI", 13, "bold"),
                         bg=self.colors["card_bg"], fg="white", anchor="w", cursor="hand2")
        title.pack(fill="x")

        artist = tk.Label(card, text=song['artist'], font=("Segoe UI", 10),
                          bg=self.colors["card_bg"], fg=self.colors["text_sub"], anchor="w", cursor="hand2")
        artist.pack(fill="x")

        # Click Logic
        def on_click(event):
            self._play_ui(song)

        def on_enter(event):
            card.config(bg=self.colors["card_hover"])
            title.config(bg=self.colors["card_hover"])
            artist.config(bg=self.colors["card_hover"])

        def on_leave(event):
            card.config(bg=self.colors["card_bg"])
            title.config(bg=self.colors["card_bg"])
            artist.config(bg=self.colors["card_bg"])

        for widget in [card, title, artist]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def _play_ui(self, song):
        success = self.recommender.play_song(song['filename'])
        if success:
            if not self.player_visible:
                self._build_player_ui()
                self.player_frame.grid(row=1, column=1, sticky="ew")
                self.player_visible = True

            self.lbl_title.config(text=song['title'])
            self.lbl_artist.config(text=song['artist'])
            self.btn_play.config(text="⏸")
        else:
            messagebox.showinfo("Missing File", f"Could not find '{song['filename']}' in songs folder.")

    def _toggle_play_pause(self):
        status = self.recommender.toggle_pause()
        if status == "playing":
            self.btn_play.config(text="⏸")
        elif status == "paused":
            self.btn_play.config(text="▶")

    def _stop_ui(self):
        self.recommender.stop_song()
        self.player_frame.grid_forget()
        self.player_visible = False

    def _show_history(self):
        self._clear_main()
        tk.Label(self.main_area, text="Your Mood Journey", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text_main"]).pack(anchor="w", pady=20)

        for m in reversed(self.user.mood_history):
            row = tk.Frame(self.main_area, bg=self.colors["card_bg"], padx=20, pady=12)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=m, bg=self.colors["card_bg"], fg=self.colors["accent_1"],
                     font=("Segoe UI", 12, "bold")).pack(side="left")

    def _clear_main(self):
        # We only clear the widgets, NOT the saved state data
        for w in self.main_area.winfo_children(): w.destroy()

    def run(self):
        self.root.mainloop()
