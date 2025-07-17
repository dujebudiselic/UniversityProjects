from observers import CursorObserver, TextObserver
import tkinter as tk

class StatusBar(TextObserver, CursorObserver):
    def __init__(self, master, model):
        self.label = tk.Label(master, bd=1, anchor=tk.W)
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
        self.model = model
        self.cursorLoc = None
        self.numLines = 0

    def updateCursorLocation(self, loc):
        self.cursorLoc = loc
        self.display()

    def updateText(self):
        self.numLines = len(self.model.getLines())
        self.display()

    def display(self):
        status = f"Ln {self.cursorLoc.getRow() + 1}, Col {self.cursorLoc.getColumn()} | {self.numLines} lines"
        self.label.config(text=status)