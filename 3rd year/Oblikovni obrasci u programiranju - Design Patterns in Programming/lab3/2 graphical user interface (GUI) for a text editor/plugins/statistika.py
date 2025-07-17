from plugin import plugin
from tkinter import messagebox

class statistika(plugin):
    def getName(self):
        return 'Statistika'

    def getDescription(self):
        return 'Prikazuje broj redaka, riječi i znakova.'

    def execute(self, model, undoManager, clipboardStack):
        lines = model.getLines()
        text = "\n".join(lines)
        numLines = len(lines)
        numWords = len(text.split())
        numCharacters = len(text)
        messagebox.showinfo('Statistika', f"Broj redaka: {numLines}\nBroj riječi: {numWords}\nBroj znakova: {numCharacters}")
