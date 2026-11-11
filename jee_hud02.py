
#!/usr/bin/env python3

import tkinter as tk
from datetime import datetime
import random
import os


# ==============================================================================
# CONFIG PANEL: CORE STATIC SETTINGS
# ==============================================================================

TARGET_YEAR = 2028
TARGET_MONTH = 1
TARGET_DAY = 1

START_YEAR = 2026
START_MONTH = 4
START_DAY = 1

# Window dimensions and placement
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 215

PADDING_RIGHT = 50
PADDING_TOP = 70

ALWAYS_ON_TOP = True
THEME_ROTATION_INTERVAL_MS = 1800000

# Score tracking
SCORE_FILE_PATH = os.path.expanduser("~/jee_scores.txt")
TARGET_SCORE = 250

PRESSURE_PHRASES = [
    "IT'S YOUR CHOICE: STUDY NOW OR REGRET LATER.",
    "YOUR COMPETITORS ARE STUDYING RIGHT NOW. WAKE UP.",
    "EVERY UNSTUDIED HOUR DROPS YOUR POTENTIAL PERCENTILE.",
    "THE TIME IS SLIPPING AWAY. WILL YOU FAIL OR EXECUTE?",
    "YOU CANNOT CHEAT THE GRIND. IT KNOWS HOW MUCH YOU WORKED.",
    "DON'T CRY LATER IF YOU CAN'T WORK HARD NOW."
]

THEMES = [
    {
        "name": "CYBERPUNK PINK",
        "border": "#FF007F",
        "bg": "#0D0A10",
        "muted": "#6B5B7B",
        "prep": "#00F0FF",
        "critical": "#FF0055",
        "decay_fill": "#FF3300"
    },
    {
        "name": "CRIMSON FURY",
        "border": "#FF1111",
        "bg": "#0F0505",
        "muted": "#542222",
        "prep": "#FFAA00",
        "critical": "#FF0033",
        "decay_fill": "#E60000"
    },
    {
        "name": "MATRIX GREEN",
        "border": "#00FF66",
        "bg": "#050A05",
        "muted": "#224422",
        "prep": "#33FF33",
        "critical": "#00FF66",
        "decay_fill": "#00CC44"
    },
    {
        "name": "VAPORWAVE BLUE",
        "border": "#7B2CBF",
        "bg": "#10002B",
        "muted": "#5A189A",
        "prep": "#00F5D4",
        "critical": "#9D4EDD",
        "decay_fill": "#240046"
    },
    {
        "name": "DEEP SPACE",
        "border": "#0077B6",
        "bg": "#03045E",
        "muted": "#0096C7",
        "prep": "#90E0EF",
        "critical": "#00B4D8",
        "decay_fill": "#00B4D8"
    }
]


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================

class JEEMainsCountdownHUD:

    def __init__(self, root):

        self.root = root

        self.start_date = datetime(
            START_YEAR, START_MONTH, START_DAY, 0, 0, 0
        )

        self.target_date = datetime(
            TARGET_YEAR, TARGET_MONTH, TARGET_DAY, 0, 0, 0
        )

        self.total_window_seconds = (
            self.target_date - self.start_date
        ).total_seconds()

        self.current_theme_index = random.randint(
            0, len(THEMES) - 1
        )

        self.theme = THEMES[self.current_theme_index]

        # Window settings
        self.root.title("JEE 2028 Tracker Engine")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", ALWAYS_ON_TOP)

        if not ALWAYS_ON_TOP:
            self.root.attributes("-type", "desktop")

        self.root.configure(bg=self.theme["border"])

        screen_width = self.root.winfo_screenwidth()

        pos_x = screen_width - WINDOW_WIDTH - PADDING_RIGHT

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{PADDING_TOP}"
        )

        # Main frame
        self.main_frame = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )

        # Header
        self.lbl_header = tk.Label(
            self.main_frame,
            text=f">>> TRACKER SYSTEM // ID: {self.theme['name']}",
            font=("Courier", 10, "bold"),
            fg=self.theme["muted"],
            bg=self.theme["bg"],
            anchor="w"
        )

        self.lbl_header.pack(
            fill="x",
            padx=15,
            pady=(12, 2)
        )

        # Separator
        self.canvas_line = tk.Canvas(
            self.main_frame,
            height=1,
            bg=self.theme["muted"],
            bd=0,
            highlightthickness=0
        )

        self.canvas_line.pack(
            fill="x",
            padx=15,
            pady=4
        )

        # Status
        self.lbl_status = tk.Label(
            self.main_frame,
            text="",
            font=("Courier", 11, "bold"),
            bg=self.theme["bg"],
            anchor="w"
        )

        self.lbl_status.pack(fill="x", padx=15)

        # Countdown
        self.lbl_time = tk.Label(
            self.main_frame,
            text="",
            font=("Courier", 24, "bold"),
            fg="#FFFFFF",
            bg=self.theme["bg"],
            anchor="w"
        )

        self.lbl_time.pack(fill="x", padx=15)

        # Decay bar
        self.bar_frame = tk.Frame(
            self.main_frame,
            bg=self.theme["bg"]
        )

        self.bar_frame.pack(
            fill="x",
            padx=15,
            pady=(2, 2)
        )

        self.lbl_bar_text = tk.Label(
            self.bar_frame,
            text="TIME RUNWAY BURNED: 0.0000%",
            font=("Courier", 9, "bold"),
            fg=self.theme["muted"],
            bg=self.theme["bg"],
            anchor="w"
        )

        self.lbl_bar_text.pack(
            side="top",
            fill="x"
        )

        self.usable_bar_width = WINDOW_WIDTH - 34

        self.canvas_bar = tk.Canvas(
            self.bar_frame,
            height=8,
            bg="#151515",
            bd=0,
            highlightthickness=0,
            width=self.usable_bar_width
        )

        self.canvas_bar.pack(
            side="top",
            fill="x",
            pady=(2, 2)
        )

        # Mock performance score
        self.lbl_score_tracker = tk.Label(
            self.main_frame,
            text="",
            font=("Courier", 10, "bold"),
            bg=self.theme["bg"],
            anchor="w"
        )

        self.lbl_score_tracker.pack(
            fill="x",
            padx=15,
            pady=(2, 2)
        )

        # Motivation
        self.lbl_motivation = tk.Label(
            self.main_frame,
            text="",
            font=("Courier", 9, "bold"),
            bg=self.theme["bg"],
            anchor="w",
            wraplength=WINDOW_WIDTH - 40
        )

        self.lbl_motivation.pack(
            fill="x",
            padx=15,
            pady=(4, 12)
        )

        # Window dragging
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag_window)

        # Start application loops
        self.update_countdown()
        self.rotate_theme_loop()

    # ==========================================================================
    # SCORE TRACKER
    # ==========================================================================

    def get_latest_mock_score(self):

        if not os.path.exists(SCORE_FILE_PATH):

            try:
                with open(SCORE_FILE_PATH, "w") as f:
                    f.write(
                        "150\n"
                        "# Edit this file. Put your latest mock score "
                        "(out of 300) on the first line."
                    )

                return 150

            except OSError:
                return 0

        try:
            with open(SCORE_FILE_PATH, "r") as f:
                first_line = f.readline().strip()
                score = int(first_line)

                return max(0, min(score, 300))

        except (OSError, ValueError):
            return 0

    # ==========================================================================
    # THEME ROTATION
    # ==========================================================================

    def rotate_theme_loop(self):

        self.current_theme_index = (
            self.current_theme_index + 1
        ) % len(THEMES)

        self.theme = THEMES[self.current_theme_index]

        self.root.configure(bg=self.theme["border"])

        self.main_frame.configure(bg=self.theme["bg"])

        self.lbl_header.config(
            text=f">>> TRACKER SYSTEM // ID: {self.theme['name']}",
            fg=self.theme["muted"],
            bg=self.theme["bg"]
        )

        self.canvas_line.config(bg=self.theme["muted"])

        self.lbl_status.config(bg=self.theme["bg"])
        self.lbl_time.config(bg=self.theme["bg"])
        self.bar_frame.config(bg=self.theme["bg"])

        self.lbl_bar_text.config(
            fg=self.theme["muted"],
            bg=self.theme["bg"]
        )

        self.lbl_score_tracker.config(bg=self.theme["bg"])
        self.lbl_motivation.config(bg=self.theme["bg"])

        self.force_instant_calculation_redraw()

        self.root.after(
            THEME_ROTATION_INTERVAL_MS,
            self.rotate_theme_loop
        )

    # ==========================================================================
    # COUNTDOWN ENGINE
    # ==========================================================================

    def update_countdown(self):

        now = datetime.now()

        diff = self.target_date - now

        total_seconds = int(diff.total_seconds())

        days = diff.days

        if total_seconds <= 0:

            self.lbl_status.config(
                text="[!] STATUS: EXECUTION PHASE",
                fg="#00FF00"
            )

            self.lbl_time.config(
                text="TARGET DATE REACHED",
                fg="#FFFFFF"
            )

            self.lbl_motivation.config(
                text="Take a breath. Focus on your next step.",
                fg=self.theme["muted"]
            )

            self.draw_decay_bar(100.0)

            return

        elapsed_seconds = (
            now - self.start_date
        ).total_seconds()

        decay_percentage = min(
            (elapsed_seconds / self.total_window_seconds) * 100,
            100.0
        ) if self.total_window_seconds > 0 else 0.0

        self.draw_decay_bar(decay_percentage)

        # Score calculation
        score = self.get_latest_mock_score()

        deficit = TARGET_SCORE - score

        if deficit > 0:

            score_text = (
                f"MOCK METER: {score}/300 | "
                f"DEFICIT: -{deficit} TO TARGET"
            )

            score_color = self.theme["critical"]

        else:

            score_text = (
                f"MOCK METER: {score}/300 | TARGET LOCKED"
            )

            score_color = "#00FF00"

        self.lbl_score_tracker.config(
            text=score_text,
            fg=score_color
        )

        current_phrase = random.choice(PRESSURE_PHRASES)

        # Critical phase
        if days < 7:

            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds // 60) % 60
            seconds = total_seconds % 60

            self.lbl_status.config(
                text="[!] STATUS: CRITICAL PHASE",
                fg=self.theme["critical"]
            )

            self.lbl_time.config(
                text=f"{days:02d}d {hours:02d}h "
                     f"{minutes:02d}m {seconds:02d}s",
                fg=self.theme["critical"]
            )

            self.lbl_motivation.config(
                text=current_phrase,
                fg=self.theme["critical"]
            )

            next_update_ms = 1000

        # Normal preparation phase
        else:

            self.lbl_status.config(
                text="[*] STATUS: CORE PREPARATION GRID",
                fg=self.theme["prep"]
            )

            self.lbl_time.config(
                text=f"{days} DAYS REMAINING",
                fg="#FFFFFF"
            )

            self.lbl_motivation.config(
                text=current_phrase,
                fg=self.theme["prep"]
            )

            next_update_ms = 60000

        self.root.after(
            next_update_ms,
            self.update_countdown
        )

    # ==========================================================================
    # PROGRESS BAR
    # ==========================================================================

    def draw_decay_bar(self, percentage):

        self.lbl_bar_text.config(
            text=f"TIME RUNWAY BURNED: {percentage:.4f}%"
        )

        self.canvas_bar.delete("all")

        fill_end_x = (
            percentage / 100.0
        ) * self.usable_bar_width

        self.canvas_bar.create_rectangle(
            0,
            0,
            fill_end_x,
            10,
            fill=self.theme["decay_fill"],
            width=0
        )

    # ==========================================================================
    # INSTANT REDRAW AFTER THEME CHANGE
    # ==========================================================================

    def force_instant_calculation_redraw(self):

        now = datetime.now()

        diff = self.target_date - now

        total_seconds = int(diff.total_seconds())

        days = diff.days

        elapsed_seconds = (
            now - self.start_date
        ).total_seconds()

        decay_percentage = min(
            (elapsed_seconds / self.total_window_seconds) * 100,
            100.0
        ) if self.total_window_seconds > 0 else 0.0

        self.draw_decay_bar(decay_percentage)

        if total_seconds > 0:

            if days < 7:

                self.lbl_status.config(
                    fg=self.theme["critical"]
                )

                self.lbl_time.config(
                    fg=self.theme["critical"]
                )

                self.lbl_motivation.config(
                    fg=self.theme["critical"]
                )

            else:

                self.lbl_status.config(
                    fg=self.theme["prep"]
                )

                self.lbl_motivation.config(
                    fg=self.theme["prep"]
                )

    # ==========================================================================
    # WINDOW DRAGGING
    # ==========================================================================

    def start_drag(self, event):

        self.x = event.x
        self.y = event.y

    def drag_window(self, event):

        deltax = event.x - self.x
        deltay = event.y - self.y

        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay

        self.root.geometry(f"+{x}+{y}")


# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":

    app = tk.Tk()

    HUD = JEEMainsCountdownHUD(app)

    app.mainloop()
