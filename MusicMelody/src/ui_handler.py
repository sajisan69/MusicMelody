import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Scale, ttk
import os
import time
import pygame 

from src.user_auth import UserAuth
from src.user import User
from src.mood_analyzer import MoodAnalyzer
from src.music_recommender import MusicRecommender


class UIHandler:
    def __init__(self):
        # --- THEME: BOLD INDIGO (High Contrast) ---
        self.colors = {
            "bg_sidebar": "#312E81",  # Deep Indigo (Sidebar)
            "bg_main": "#F3F4F6",  # Light Grey (Main Content BG)
            "bg_card": "#FFFFFF",  # Pure White (Cards)
            "bg_player": "#FFFFFF",  # Player Bar

            "primary": "#4338CA",  # Indigo (Primary Buttons/Accents)
            "primary_hov": "#3730A3",  # Darker Indigo
            "accent": "#E11D48",  # Rose Red (Highlights)

            "text_sidebar": "#FFFFFF",  # White text on dark sidebar
            "text_main": "#111827",  # Almost Black (Main Headings)
            "text_body": "#374151",  # Dark Grey (Readable Body Text)
            "text_sub": "#4B5563",  # Slate (Subtitles)

            "border": "#E5E7EB",  # Light Border
            "danger": "#EF4444"  # Red (Logout)
        }

        self.fonts = {
            "logo": ("Verdana", 18, "bold"),
            "h1": ("Segoe UI", 24, "bold"),
            "h2": ("Segoe UI", 16, "bold"),
            "body": ("Segoe UI", 11),
            "btn": ("Segoe UI", 10, "bold")
        }

        # Backend
        self.auth = UserAuth()
        self.recommender = MusicRecommender()
        self.analyzer = MoodAnalyzer()
        self.user_obj = None
        self.current_user = None

        # State
        self.state = {
            "last_search": "",
            "last_mood": "Daily Mix",
            "last_results": [],
            "current_song": None,
            "timer_id": None,
            "current_offset": 0  # Tracks where the song started (for seeking)
        }

        # Window
        self.root = tk.Tk()
        self.root.title("MusicMelody")
        self.root.geometry("1280x850")
        self.root.configure(bg=self.colors["bg_main"])

        self._show_login()

    # --- HELPERS ---
    def _clear_all(self):
        for w in self.root.winfo_children(): w.destroy()
        self._stop_timer()

    def _clear_content(self):
        if hasattr(self, 'content'):
            for w in self.content.winfo_children(): w.destroy()

    def _btn(self, parent, text, cmd, bg=None, fg="white", width=None):
        if not bg: bg = self.colors["primary"]
        btn = tk.Button(parent, text=text, bg=bg, fg=fg, font=self.fonts["btn"],
                        relief="flat", bd=0, padx=20, pady=12, cursor="hand2", command=cmd)
        if width: btn.config(width=width)

        def on_e(e):
            btn.config(bg=self.colors["primary_hov"] if bg == self.colors["primary"] else bg)

        def on_l(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", on_e)
        btn.bind("<Leave>", on_l)
        return btn

    def _entry(self, parent, placeholder, show=None):
        tk.Label(parent, text=placeholder, bg="white", fg=self.colors["text_body"],
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(15, 5))
        wrapper = tk.Frame(parent, bg=self.colors["text_sub"], padx=1, pady=1)
        wrapper.pack(fill="x")
        e = tk.Entry(wrapper, font=("Segoe UI", 12), bg="white", fg="black", relief="flat", show=show)
        e.pack(fill="x", ipady=8, ipadx=5)
        return e

    # --- AUTH ---
    def _show_login(self):
        self._clear_all()
        bg_top = tk.Frame(self.root, bg=self.colors["bg_sidebar"], height=300)
        bg_top.place(x=0, y=0, relwidth=1)

        card = tk.Frame(self.root, bg="white", padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="MusicMelody", font=self.fonts["logo"], bg="white", fg=self.colors["primary"]).pack()
        tk.Label(card, text="Premium Audio Experience", font=("Segoe UI", 10), bg="white",
                 fg=self.colors["text_sub"]).pack(pady=(0, 25))

        self.u_in = self._entry(card, "Username")
        self.p_in = self._entry(card, "Password", show="*")

        self._btn(card, "LOG IN", self._login_act).pack(fill="x", pady=25)

        link = tk.Label(card, text="Create an Account", bg="white", fg=self.colors["primary"], cursor="hand2",
                        font=("Segoe UI", 10, "underline"))
        link.pack()
        link.bind("<Button-1>", lambda e: self._show_signup())

    def _show_signup(self):
        self._clear_all()
        bg_top = tk.Frame(self.root, bg=self.colors["bg_sidebar"], height=300)
        bg_top.place(x=0, y=0, relwidth=1)

        card = tk.Frame(self.root, bg="white", padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Join Us", font=self.fonts["logo"], bg="white", fg=self.colors["primary"]).pack(
            pady=(0, 20))
        self.u_in = self._entry(card, "Pick a Username")
        self.p_in = self._entry(card, "Pick a Password", show="*")
        self._btn(card, "SIGN UP", self._signup_act).pack(fill="x", pady=25)
        link = tk.Label(card, text="Back to Login", bg="white", fg=self.colors["text_sub"], cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: self._show_login())

    def _login_act(self):
        u, p = self.u_in.get(), self.p_in.get()
        if self.auth.login(u, p)[0]:
            self.current_user = u
            self.user_obj = User(u)
            self._init_main()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def _signup_act(self):
        if self.auth.signup(self.u_in.get(), self.p_in.get())[0]:
            messagebox.showinfo("Success", "Account Created");
            self._show_login()

    # --- MAIN LAYOUT ---
    def _init_main(self):
        self._clear_all()
        self.sidebar = tk.Frame(self.root, bg=self.colors["bg_sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.content.pack(side="top", fill="both", expand=True)

        self.player = tk.Frame(self.root, bg=self.colors["bg_player"], height=90)
        self.player.pack(side="bottom", fill="x")
        self.player.pack_propagate(False)
        self._draw_player()

        # Sidebar
        logo_box = tk.Frame(self.sidebar, bg=self.colors["bg_sidebar"], pady=40)
        logo_box.pack(fill="x")
        tk.Label(logo_box, text="MusicMelody", font=self.fonts["logo"], bg=self.colors["bg_sidebar"], fg="white").pack()

        self._nav_btn("Dashboard", self._view_dash, icon="🏠")
        self._nav_btn("My Uploads", self._view_my_uploads, icon="☁")
        self._nav_btn("Add Music", self._view_add, icon="➕")
        self._nav_btn("History", self._view_hist, icon="🕒")

        tk.Frame(self.sidebar, bg=self.colors["bg_sidebar"]).pack(fill="both", expand=True)
        self._nav_btn("Log Out", self._show_login, color="#EF4444", icon="🚪")

        self._view_dash()

    def _nav_btn(self, text, cmd, color="white", icon=""):
        btn = tk.Button(self.sidebar, text=f"  {icon}   {text}", font=("Segoe UI", 11, "bold"),
                        bg=self.colors["bg_sidebar"], fg=color,
                        activebackground="#4338CA", activeforeground="white",
                        bd=0, anchor="w", padx=30, pady=15, cursor="hand2", command=cmd)
        btn.pack(fill="x")

    # --- DASHBOARD ---
    def _view_dash(self):
        self._clear_content()
        self._header(f"Welcome back, {self.current_user}")

        search_box = tk.Frame(self.content, bg="white", padx=20, pady=20)
        search_box.pack(fill="x", padx=40, pady=(0, 20))

        inp_frame = tk.Frame(search_box, bg=self.colors["text_sub"], padx=1, pady=1)
        inp_frame.pack(side="left", fill="x", expand=True, padx=(0, 15))

        self.search_in = tk.Entry(inp_frame, font=("Segoe UI", 14), bg="white", fg="black", relief="flat")
        self.search_in.pack(fill="both", ipady=10, ipadx=10)
        if self.state["last_search"]: self.search_in.insert(0, self.state["last_search"])

        self._btn(search_box, "ANALYZE MOOD", self._analyze, width=20).pack(side="right")

        self.list_area = tk.Frame(self.content, bg=self.colors["bg_main"])
        self.list_area.pack(fill="both", expand=True, padx=40)

        if not self.state["last_results"]:
            self.state["last_results"] = self.recommender.get_all_songs()
            self.state["last_mood"] = "Your Daily Mix"

        self._render_list(self.state["last_mood"], self.state["last_results"])

    def _analyze(self):
        txt = self.search_in.get()
        if not txt:
            self.state["last_results"] = self.recommender.get_all_songs()
            self.state["last_mood"] = "Your Daily Mix"
        else:
            self.state["last_search"] = txt
            m = self.analyzer.analyze_mood(txt)
            self.state["last_mood"] = f"Current Vibe: {m}"
            self.state["last_results"] = self.recommender.get_recommendations(m)
        self._render_list(self.state["last_mood"], self.state["last_results"])

    def _render_list(self, title, songs, show_mood_tag=False):
        for w in self.list_area.winfo_children(): w.destroy()

        tk.Label(self.list_area, text=title, font=self.fonts["h2"], bg=self.colors["bg_main"],
                 fg=self.colors["primary"]).pack(anchor="w", pady=(0, 15))

        canvas = Canvas(self.list_area, bg=self.colors["bg_main"], highlightthickness=0)
        sb = ttk.Scrollbar(self.list_area, orient="vertical", command=canvas.yview)
        fr = tk.Frame(canvas, bg=self.colors["bg_main"])

        fr.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=fr, anchor="nw", width=900)
        canvas.configure(yscrollcommand=sb.set)

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        if not songs:
            tk.Label(fr, text="No songs found.", bg=self.colors["bg_main"], fg=self.colors["text_body"]).pack()

        for s in songs: self._card(fr, s, show_mood_tag)

    def _card(self, parent, song, show_mood_tag=False):
        c = tk.Frame(parent, bg="white", padx=20, pady=15)
        c.pack(fill="x", pady=8)

        accent_bar = tk.Frame(c, bg=self.colors["accent"], width=5)
        accent_bar.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(c, text="▶", font=("Arial", 14), bg="white", fg=self.colors["primary"]).pack(side="left", padx=(0, 15))

        info = tk.Frame(c, bg="white")
        info.pack(side="left", fill="x", expand=True)

        tk.Label(info, text=song['title'], font=("Segoe UI", 12, "bold"), bg="white", fg="black", anchor="w").pack(
            fill="x")
        tk.Label(info, text=song['artist'], font=("Segoe UI", 11), bg="white", fg=self.colors["text_body"],
                 anchor="w").pack(fill="x")

        btn = tk.Button(c, text="Play", bg=self.colors["bg_main"], fg="black", bd=0, padx=15, pady=5, cursor="hand2",
                        command=lambda: self._play(song))
        btn.pack(side="right")

        if show_mood_tag:
            found_mood = "Unknown"
            for m_key, s_list in self.recommender.music_db.items():
                if song in s_list: found_mood = m_key; break

            lbl_mood = tk.Label(c, text=found_mood.upper(), bg="#E0E7FF", fg=self.colors["primary"],
                                font=("Segoe UI", 8, "bold"), padx=8, pady=4)
            lbl_mood.pack(side="right", padx=15)

        def play_click(e):
            self._play(song)

        c.bind("<Button-1>", play_click)
        info.bind("<Button-1>", play_click)

    # --- MY UPLOADS ---
    def _view_my_uploads(self):
        self._clear_content()
        self._header("My Uploads")
        self.list_area = tk.Frame(self.content, bg=self.colors["bg_main"])
        self.list_area.pack(fill="both", expand=True, padx=40)
        my_songs = self.recommender.get_user_uploads(self.current_user)
        self._render_list("Songs You Added", my_songs, show_mood_tag=True)

    # --- ADD MUSIC ---
    def _view_add(self):
        self._clear_content()
        self._header("Upload New Music")

        f = tk.Frame(self.content, bg="white", padx=40, pady=40)
        f.pack(fill="x", padx=40)

        self.add_t = self._entry(f, "Song Title")
        self.add_a = self._entry(f, "Artist Name")

        tk.Label(f, text="Select Song Vibe", bg="white", fg=self.colors["text_body"],
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(15, 5))

        self.mood_var = tk.StringVar()
        self.mood_combo = ttk.Combobox(f, textvariable=self.mood_var, font=("Segoe UI", 11), state="readonly")
        self.mood_combo['values'] = ("Happy", "Sad", "Calm", "Energetic", "Focus", "Party", "Romantic")
        self.mood_combo.current(0)
        self.mood_combo.pack(fill="x", ipady=4)

        self.lbl_f = tk.Label(f, text="No file selected", bg="white", fg="red", font=("Segoe UI", 10, "bold"))
        self.lbl_f.pack(pady=10)

        tk.Button(f, text="Select MP3 File", command=self._pick_file, bg=self.colors["bg_main"], fg="black", bd=0,
                  padx=20, pady=10).pack()
        self._btn(f, "UPLOAD NOW", self._do_upload).pack(fill="x", pady=25)

    def _pick_file(self):
        p = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3")])
        if p:
            self.fp = p
            self.lbl_f.config(text=f"Selected: {os.path.basename(p)}", fg="green")

    def _do_upload(self):
        mood_val = self.mood_var.get()
        if not (self.add_t.get() and hasattr(self, 'fp') and mood_val): return
        ok, msg = self.recommender.add_song(self.add_t.get(), self.add_a.get(), mood_val, self.fp, self.current_user)
        if ok:
            messagebox.showinfo("Success", "Song Uploaded!")
            self._view_my_uploads()
        else:
            messagebox.showerror("Error", msg)

    def _view_hist(self):
        self._clear_content()
        self._header("Listening History")
        h_area = tk.Frame(self.content, bg="white", padx=20, pady=20)
        h_area.pack(fill="both", expand=True, padx=40, pady=10)

        self.user_obj.history = self.user_obj._load_history()
        for i, item in enumerate(self.user_obj.history):
            bg_col = "#F9FAFB" if i % 2 == 0 else "white"
            row = tk.Frame(h_area, bg=bg_col, pady=12, padx=10)
            row.pack(fill="x")

            tk.Label(row, text=item['title'], width=30, anchor="w", font=("Segoe UI", 11, "bold"), bg=bg_col,
                     fg="black").pack(side="left")
            tk.Label(row, text=item['timestamp'], font=("Segoe UI", 10), bg=bg_col, fg=self.colors["text_body"]).pack(
                side="right")

    # --- PLAYER & LOGIC ---
    def _header(self, t):
        tk.Label(self.content, text=t, font=self.fonts["h1"], bg=self.colors["bg_main"],
                 fg=self.colors["text_main"]).pack(anchor="w", padx=40, pady=30)

    def _play(self, s):
        if self.recommender.play_song(s['filename'])[0]:
            self.user_obj.log_song(s)
            self.state["current_song"] = s
            self.state["current_offset"] = 0  # Reset seek offset

            self._stop_timer()
            self._draw_player(s)
            self._start_timer()
        else:
            messagebox.showerror("Error", "File not found")

    def _seek(self, seconds):
        """Standard Pygame doesn't seek easily. We track start time + offset."""
        if not self.state["current_song"]: return

        # 1. Calculate current play position + jump
        # get_pos returns ms played since last 'play'. Add that to our accumulated offset.
        current_playback_pos = pygame.mixer.music.get_pos() / 1000  # convert to seconds
        new_start_time = self.state["current_offset"] + current_playback_pos + seconds

        if new_start_time < 0: new_start_time = 0

        # 2. Update Offset
        self.state["current_offset"] = new_start_time

        # 3. Reload and Restart from new time
        # Note: We need the full path. Recommender usually handles this, but for seeking
        # we need direct control or a robust seek function.
        # We will use the recommender's loaded file logic if possible,
        # but here we rely on the filename stored in song dict.
        try:
            pygame.mixer.music.play(start=new_start_time)
        except Exception as e:
            # If start time is beyond song duration, it might stop or error.
            print(f"Seek Error: {e}")

    def _draw_player(self, s=None):
        for w in self.player.winfo_children(): w.destroy()

        # --- NEW: LOGO BOX ---
        logo_area = tk.Frame(self.player, bg=self.colors["primary"], width=80, height=80)
        logo_area.pack(side="left", padx=(20, 15), pady=5)
        logo_area.pack_propagate(False)  # Force size
        # A big music note character as a logo
        tk.Label(logo_area, text="🎵", font=("Segoe UI", 30), bg=self.colors["primary"], fg="white").place(relx=0.5,
                                                                                                          rely=0.5,
                                                                                                          anchor="center")

        # Info
        info = tk.Frame(self.player, bg="white")
        info.pack(side="left", padx=10)
        tk.Label(info, text=s['title'] if s else "Ready to Jam", font=("Segoe UI", 12, "bold"), bg="white",
                 fg="black").pack(anchor="w")
        tk.Label(info, text=s['artist'] if s else "Select a track...", font=("Segoe UI", 10), bg="white",
                 fg=self.colors["text_body"]).pack(anchor="w")

        # Controls
        ctrl = tk.Frame(self.player, bg="white")
        ctrl.pack(side="left", expand=True)

        btn_style = {"bg": "white", "fg": "black", "bd": 0, "font": ("Arial", 16), "cursor": "hand2"}

        # Rewind (-10s)
        tk.Button(ctrl, text="⏪", command=lambda: self._seek(-10), **btn_style).pack(side="left", padx=10)

        # Play/Pause
        self.btn_p = tk.Button(ctrl, text="⏸" if s else "▶", command=self._tog,
                               bg=self.colors["primary"], fg="white", bd=0, font=("Arial", 14), width=5, height=1)
        self.btn_p.pack(side="left", padx=15)

        # Forward (+10s)
        tk.Button(ctrl, text="⏩", command=lambda: self._seek(10), **btn_style).pack(side="left", padx=10)

        # Time
        self.lbl_time = tk.Label(ctrl, text="00:00", font=("Segoe UI", 12, "bold"), bg="white",
                                 fg=self.colors["primary"])
        self.lbl_time.pack(side="left", padx=(25, 0))

        # Volume
        vol = tk.Frame(self.player, bg="white")
        vol.pack(side="right", padx=30)
        tk.Label(vol, text="Vol", bg="white", fg="black").pack(side="left")
        Scale(vol, from_=0, to=1, resolution=0.1, orient="horizontal", bg="white", fg=self.colors["primary"],
              command=self.recommender.set_volume, showvalue=0, length=100, highlightthickness=0,
              troughcolor="#E5E7EB").pack()

    def _tog(self):
        st = self.recommender.toggle_pause()
        self.btn_p.config(text="⏸" if st == "playing" else "▶")
        if st == "playing": self._start_timer()

    # --- TIMER LOGIC (UPDATED FOR SEEKING) ---
    def _start_timer(self):
        self._stop_timer()
        self._update_timer_loop()

    def _stop_timer(self):
        if self.state["timer_id"]:
            self.root.after_cancel(self.state["timer_id"])
            self.state["timer_id"] = None

    def _update_timer_loop(self):
        if pygame.mixer.music.get_busy():
            # Current time = Start Offset (from seeking) + Playback Time (since last play/seek)
            play_ms = pygame.mixer.music.get_pos()
            if play_ms == -1: play_ms = 0

            total_seconds = int(self.state["current_offset"] + (play_ms / 1000))

            formatted = time.strftime('%M:%S', time.gmtime(total_seconds))

            if hasattr(self, 'lbl_time'): self.lbl_time.config(text=formatted)

            self.state["timer_id"] = self.root.after(1000, self._update_timer_loop)
        else:
            # Only reset if we assume song finished naturally.
            pass

    def run(self):
        self.root.mainloop()
