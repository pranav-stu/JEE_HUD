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

# Window Dimensions & Placement
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 160
PADDING_RIGHT = 50   # Pixels away from the right edge of the screen
PADDING_TOP = 70     # Pixels away from the top edge of the screen

# Feature Toggles
ALWAYS_ON_TOP = False  # Set to True to float above ALL windows. Set to False to sit on desktop wallpaper.

# Color Themes (Uncomment the one you want to use, or make your own!)
# Hot Pink / Purple Grid Theme
BORDER_COLOR = "#FF007F"      # Vibrant Hot Pink Border
BG_COLOR = "#0D0A10"          # Deep Cyber Dark Violet-Grey Background
TEXT_MUTED = "#6B5B7B"        # Muted purple for metadata/labels
COLOR_PREP = "#00F0FF"        # Cyan Blue for the core study phase
COLOR_CRITICAL = "#FF0055"    # Blazing neon red for the < 7 days panic phase

# Alternate Theme Example (To use it, uncomment below and comment out the pink ones above):
# BORDER_COLOR = "#00FF66"    # Neon Matrix Green
# BG_COLOR = "#0A0F0D"        # Pitch Black-Green

# Psychological Pressure Phrases (One will be selected randomly every time the timer updates)
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
        
        # Parse the configuration targets into a native datetime object
        self.target_date = datetime(TARGET_YEAR, TARGET_MONTH, TARGET_DAY, 0, 0, 0)
        
        # Window configuration setup
        self.root.title("JEE 2028 Tracker")
        self.root.overrideredirect(True) # Disables OS title bars and window control buttons
        
        # 1) ALWAYS ON TOP TOGGLE ENGINE
        # Intercepts window state management flags directly from your OS window manager
        self.root.wm_attributes("-topmost", ALWAYS_ON_TOP)
        if not ALWAYS_ON_TOP:
            self.root.attributes("-type", "desktop") # Locks widget to wallpaper layer if topmost is disabled

        # 2) ACCENT WINDOW BORDER ARCHITECTURE
        # We simulate a modern sleek border by coloring the true window background (BG_COLOR/BORDER_COLOR)
        # and creating an internal frame with minor padding to build a high-contrast bezel line.
        self.root.configure(bg=BORDER_COLOR)
        
        # Position calculations matching your native screen resolution scale
        screen_width = self.root.winfo_screenwidth()
        pos_x = screen_width - WINDOW_WIDTH - PADDING_RIGHT
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{pos_x}+{PADDING_TOP}")
        
        # Main inner container box
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2) # Change padx/pady to adjust border thickness
        
        # 3) INTERFACE LABELS & TYPOGRAPHY LAYOUT (ASCII Replace for failing emoji icons)
        self.lbl_header = tk.Label(self.main_frame, text=">>> METRIC TRACKER // JEE MAINS 2028", 
                                   font=("Courier", 10, "bold"), fg=TEXT_MUTED, bg=BG_COLOR, anchor="w")
        self.lbl_header.pack(fill="x", padx=15, pady=(12, 2))
        
        # Sleek UI horizontal dividing line separator
        self.canvas_line = tk.Canvas(self.main_frame, height=1, bg=TEXT_MUTED, bd=0, highlightthickness=0)
        self.canvas_line.pack(fill="x", padx=15, pady=4)
        
        self.lbl_status = tk.Label(self.main_frame, text="", font=("Courier", 11, "bold"), bg=BG_COLOR, anchor="w")
        self.lbl_status.pack(fill="x", padx=15)
        
        self.lbl_time = tk.Label(self.main_frame, text="", font=("Courier", 24, "bold"), fg="#FFFFFF", bg=BG_COLOR, anchor="w")
        self.lbl_time.pack(fill="x", padx=15)
        
        self.lbl_motivation = tk.Label(self.main_frame, text="", font=("Courier", 9, "bold"), bg=BG_COLOR, anchor="w", wraplength=WINDOW_WIDTH-40)
        self.lbl_motivation.pack(fill="x", padx=15, pady=(4, 12))
        
        # Interactive dragging engine hooks to move the window if needed
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag_window)
        
        # Initialize execution tracking loop
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
            return

        # Choose a random pressure phrase to rotate mind games on each phase check
        current_phrase = random.choice(PRESSURE_PHRASES)

        # CASE A: CRITICAL COUNTDOWN MODE (Less than 7 Days remaining)
        if days < 7:
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds // 60) % 60
            seconds = total_seconds % 60
            
            self.lbl_status.config(text="[!] STATUS: CRITICAL PHASE", fg=COLOR_CRITICAL)
            self.lbl_time.config(text=f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s", fg=COLOR_CRITICAL)
            self.lbl_motivation.config(text=current_phrase, fg=COLOR_CRITICAL)
            next_update_ms = 1000 # High-speed updates (1 second) to force real-time ticking pressure
            
        # CASE B: GRID PREPARATION MODE (More than 7 Days remaining)
        else:
            self.lbl_status.config(text="[*] STATUS: CORE PREPARATION GRID", fg=COLOR_PREP)
            self.lbl_time.config(text=f"{days} DAYS REMAINING", fg="#FFFFFF")
            self.lbl_motivation.config(text=current_phrase, fg=COLOR_PREP)
            next_update_ms = 60000 # Micro-optimized sleep window (1 minute update) to save CPU/RAM cycles

        # Enqueue the next calculations execution sweep into Tkinter's internal callback framework
        self.root.after(next_update_ms, self.update_countdown)

    # Mouse positional mapping algorithms to track moving operations
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
