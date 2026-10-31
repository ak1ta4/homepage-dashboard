"""Task reminder window opened by the agent.

Usage: pythonw reminder_popup.py <title> <text> [slot]
Bottom-right corner of the main screen, always on top, stays until clicked.
`slot` stacks several reminders upwards.
"""
import ctypes
import sys
import tkinter as tk
import tkinter.font as tkfont
import winsound
from ctypes import wintypes

title = sys.argv[1]
text = sys.argv[2]
slot = int(sys.argv[3]) if len(sys.argv) > 3 else 0

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, OSError):
    pass

BG, LINE, FG, DIM, ACCENT = "#0F0F0F", "#3A3A3A", "#FFFFFF", "#A8A8A8", "#E8622C"

root = tk.Tk()
root.withdraw()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg=LINE)  # 1px outline around the card

families = set(tkfont.families())
mono = next((f for f in ("Space Mono", "Consolas") if f in families), "Courier New")
sans = next((f for f in ("Space Grotesk", "Segoe UI") if f in families), "Arial")

card = tk.Frame(root, bg=BG, padx=18, pady=14)
card.pack(padx=1, pady=1)
tk.Frame(card, bg=ACCENT, width=28, height=2).pack(anchor="w", pady=(0, 10))
tk.Label(card, text=title.upper(), bg=BG, fg=DIM, font=(mono, 9)).pack(anchor="w")
tk.Label(card, text=text, bg=BG, fg=FG, font=(sans, 13), wraplength=340, justify="left").pack(anchor="w", pady=(6, 8))
tk.Label(card, text="CLICK TO DISMISS", bg=BG, fg=DIM, font=(mono, 8)).pack(anchor="e")


def close(_=None):
    root.destroy()


root.bind_all("<Button-1>", close)

root.update_idletasks()
area = wintypes.RECT()
ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(area), 0)  # SPI_GETWORKAREA: excludes the taskbar
w, h = root.winfo_reqwidth(), root.winfo_reqheight()
root.geometry(f"+{area.right - w - 16}+{area.bottom - h - 16 - slot * (h + 10)}")
root.deiconify()
winsound.MessageBeep(winsound.MB_ICONASTERISK)
root.mainloop()
