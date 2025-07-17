import tkinter as tk
from texteditormodel import TextEditorModel
from clipboard import ClipboardStack
from texteditor import TextEditor
from statusbar import StatusBar
from undomanager import UndoManager

def main():
    master = tk.Tk()
    master.title('TextEditor')
    text = 'Ovo je 3. labos iz ooup.\nNadam se da ću dobiti što vise bodova!\nHvala...'
    textEditorModelmodel = TextEditorModel(text)
    statusbar = StatusBar(master, textEditorModelmodel)
    clipboard = ClipboardStack()
    texteditor = TextEditor(master, textEditorModelmodel, clipboard)
    #texteditor = TextEditor(master, textEditorModelmodel, clipboard, 2, 3)
    UndoManager.getInstance().addObserver(texteditor)
    textEditorModelmodel.addCursorObserver(texteditor)
    textEditorModelmodel.addTextObserver(texteditor)
    textEditorModelmodel.addCursorObserver(statusbar)
    textEditorModelmodel.addTextObserver(statusbar)
    clipboard.addObserver(texteditor)
    master.mainloop()

if __name__ == '__main__':
    main()