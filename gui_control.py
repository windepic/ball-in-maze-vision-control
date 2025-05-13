"""
Note: This GUI interface (Tkinter) was NOT developed by me personally.
It is included here solely for completeness of the project.
"""

import tkinter as tk
from PIL import Image, ImageTk

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball Maze Controller")
        self.root.geometry("900x500")
        self.root.configure(bg="white")
        self.frames = {}

        self.main_frame = tk.Frame(self.root, bg="white")
        self._build_main_menu()

    def _build_main_menu(self):
        tk.Label(self.main_frame, text="Auto-maze Project", font=("Times New Roman", 18, "bold"), bg="white").pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.root.quit).pack(pady=20)
        self.main_frame.pack()

    def show_main(self):
        self._hide_all()
        self.main_frame.pack()

    def _hide_all(self):
        for frame in self.frames.values():
            frame.pack_forget()
