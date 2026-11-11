#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import random

# ==============================================================================
# CONFIG PANEL: MODIFY THESE VALUES TO CUSTOMIZE YOUR DASHBOARD
# ==============================================================================
# Target Exam Date (Expected Session 1: January 1, 2028, at midnight)
TARGET_YEAR = 2028
TARGET_MONTH = 1
TARGET_DAY = 1

# Progress Bar Anchor: The date you started preparing seriously for JEE
START_YEAR = 2026
START_MONTH = 5
START_DAY = 1

# Window Dimensions & Placement
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 190
PADDING_RIGHT = 50   # Pixels away from the right edge of the screen
PADDING_TOP = 70     # Pixels away from the top edge of the screen


# Feature Toggles
ALWAYS_ON_TOP = False  # True to float above all windows. False to sit on wallpaper.

# Color Themes
BORDER_COLOR = "#FF007F"      # Vibrant Hot Pink Border
BG_COLOR = "#0D0A10"          # Deep Cyber Dark Violet-Grey Background
TEXT_MUTED = "#6B5B7B"        # Muted purple for metadata/labels
COLOR_PREP = "#00F0FF"        # Cyan Blue for the core study phase
COLOR_CRITICAL = "#FF0055"    # Neon red for the < 7 days panic phase
BAR_DECAY_FILL = "#FF3300"    # High-pressure orange-red for consumed time

# Psychological Pressure Phrases
PRESSURE_PHRASES = [
    "IT'S YOUR CHOICE: STUDY NOW OR REGRET LATER.",
    "YOUR COMPETITORS ARE STUDYING RIGHT NOW. WAKE UP.",
    "EVERY UNSTUDIED HOUR DROPS YOUR POTENTIAL PERCENTILE.",
    "THE TIME IS SLIPPING AWAY. WILL YOU FAIL OR EXECUTE?",
    "YOU CANNOT CHEAT THE GRIND. IT KNOWS HOW MUCH YOU WORKED.",
    "DON'T CRY LATER IF YOU CAN'T WORK HARD NOW."
]
# ==============================================================================

class JEEMainsCountdownHUD:
    def __init__(self, root):
        self.root = root
        
        # Parse dates safely at initialization
        self.start_date = datetime(START_YEAR, START_MONTH, START_DAY, 0, 0, 0)
        self.target_date = datetime(TARGET_YEAR, TARGET_MONTH, TARGET_DAY, 0, 0, 0)
        
        # Precompute window metrics
        self.total_window_seconds = (self.target_date - self.start_date).total_seconds()
        
        # Window configuration setup
        self.root.title("JEE 2028 Tracker Engine")
        self.root.overrideredirect(True) 
        self.root.wm_attributes("-topmost", ALWAYS_ON_TOP)
        
        if not ALWAYS_ON_TOP:
            self.root.attributes("-type", "desktop")

        self.root.configure(bg=BORDER_COLOR)
        
        # Position mapping
        screen_width = self.root.winfo_screenwidth()
        pos_x = screen_width - WINDOW_WIDTH - PADDING_RIGHT
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{PADDING_TOP}")
        
        # Main inner frame
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Typographic Layout Setup
        self.lbl_header = tk.Label(self.main_frame, text=">>> METRIC TRACKER // JEE MAINS 2028", 
                                   font=("Courier", 10, "bold"), fg=TEXT_MUTED, bg=BG_COLOR, anchor="w")
        self.lbl_header.pack(fill="x", padx=15, pady=(12, 2))
        
        self.canvas_line = tk.Canvas(self.main_frame, height=1, bg=TEXT_MUTED, bd=0, highlightthickness=0)
        self.canvas_line.pack(fill="x", padx=15, pady=4)
        
        self.lbl_status = tk.Label(self.main_frame, text="", font=("Courier", 11, "bold"), bg=BG_COLOR, anchor="w")
        self.lbl_status.pack(fill="x", padx=15)
        
        self.lbl_time = tk.Label(self.main_frame, text="", font=("Courier", 24, "bold"), fg="#FFFFFF", bg=BG_COLOR, anchor="w")
        self.lbl_time.pack(fill="x", padx=15)
        
        # Progress Bar Layout
        self.bar_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.bar_frame.pack(fill="x", padx=15, pady=(4, 2))
        
        self.lbl_bar_text = tk.Label(self.bar_frame, text="TIME RUNWAY BURNED: 0.0000%", 
                                     font=("Courier", 9, "bold"), fg=TEXT_MUTED, bg=BG_COLOR, anchor="w")
        self.lbl_bar_text.pack(side="top", fill="x")
        
        self.usable_bar_width = WINDOW_WIDTH - 34
        
        self.canvas_bar = tk.Canvas(self.bar_frame, height=10, bg="#221A28", bd=0, highlightthickness=0, width=self.usable_bar_width)
        self.canvas_bar.pack(side="top", fill="x", pady=(2, 2))
        
        self.lbl_motivation = tk.Label(self.main_frame, text="", font=("Courier", 9, "bold"), bg=BG_COLOR, anchor="w", wraplength=WINDOW_WIDTH-40)
        self.lbl_motivation.pack(fill="x", padx=15, pady=(4, 12))
        
        # Drag bindings
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag_window)
        
        # Start core loop
        self.update_countdown()

    def update_countdown(self):
        now = datetime.now()
        diff = self.target_date - now
        total_seconds = int(diff.total_seconds())
        days = diff.days
        
        if total_seconds <= 0:
            self.lbl_status.config(text="[!] STATUS: EXECUTION PHASE", fg="#00FF00")
            self.lbl_time.config(text="🎯 TIME IS NOW", fg="#FFFFFF")
            self.lbl_motivation.config(text="No more excuses. Execute cleanly on the paper.", fg=TEXT_MUTED)
            self.draw_decay_bar(100.0)
            return

        elapsed_seconds = (now - self.start_date).total_seconds()
        if self.total_window_seconds > 0 and elapsed_seconds > 0:
            decay_percentage = min((elapsed_seconds / self.total_window_seconds) * 100, 100.0)
        else:
            decay_percentage = 0.0
            
        self.draw_decay_bar(decay_percentage)
        current_phrase = random.choice(PRESSURE_PHRASES)

        # CASE A: CRITICAL PREPARATION PHASE (< 7 Days Remaining)
        if days < 7:
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds // 60) % 60
            seconds = total_seconds % 60
            
            self.lbl_status.config(text="[!] STATUS: CRITICAL PHASE", fg=COLOR_CRITICAL)
            self.lbl_time.config(text=f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s", fg=COLOR_CRITICAL)
            self.lbl_motivation.config(text=current_phrase, fg=COLOR_CRITICAL)
            next_update_ms = 1000
            
        # CASE B: LONG-TERM GRID PREPARATION
        else:
            self.lbl_status.config(text="[*] STATUS: CORE PREPARATION GRID", fg=COLOR_PREP)
            self.lbl_time.config(text=f"{days} DAYS REMAINING", fg="#FFFFFF")
            self.lbl_motivation.config(text=current_phrase, fg=COLOR_PREP)
            next_update_ms = 60000

        self.root.after(next_update_ms, self.update_countdown)

    def draw_decay_bar(self, percentage):
        self.lbl_bar_text.config(text=f"TIME RUNWAY BURNED: {percentage:.4f}%")
        self.canvas_bar.delete("all")
        fill_end_x = (percentage / 100.0) * self.usable_bar_width
        
        # Borderless Canvas Rectangle Fix (uses width=0 instead of borderwidth=0)
        self.canvas_bar.create_rectangle(0, 0, fill_end_x, 10, fill=BAR_DECAY_FILL, width=0)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag_window(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = tk.Tk()
    HUD = JEEMainsCountdownHUD(app)
    app.mainloop()
