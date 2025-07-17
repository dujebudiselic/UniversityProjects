import tkinter as tk
from tkinter import filedialog
from observers import CursorObserver, TextObserver, UndoObserver, ClipboardObserver
from undomanager import UndoManager
from getplugins import getPlugins
from location import Location, LocationRange

class TextEditor(tk.Canvas, CursorObserver, TextObserver, UndoObserver, ClipboardObserver):
    def __init__(self, master, model, clipboard, index1 = 0, index2 = 0):
        super().__init__(master, width=500, height=500, bg='white')
        self.master = master
        self.model = model
        self.clipboard = clipboard
        self.index1 = index1
        self.index2 = index2

        self.canUndo = False
        self.canRedo = False

        self.toolbar = tk.Frame(self.master, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.undoButton = tk.Button(self.toolbar, text='Undo', state='disabled', command=lambda: self.obaviUndo(None))
        self.undoButton.pack(side=tk.LEFT, padx=2, pady=2)

        self.redoButton = tk.Button(self.toolbar, text='Redo', state='disabled', command=lambda: self.obaviRedo(None))
        self.redoButton.pack(side=tk.LEFT, padx=2, pady=2)

        self.cutButton = tk.Button(self.toolbar, text='Cut', state='disabled', command=lambda: self.cutselectionRange(None))
        self.cutButton.pack(side=tk.LEFT, padx=2, pady=2)

        self.copyButton = tk.Button(self.toolbar, text='Copy', state='disabled', command=lambda: self.copyselectionRange(None))
        self.copyButton.pack(side=tk.LEFT, padx=2, pady=2)

        self.pasteButton = tk.Button(self.toolbar, text='Paste', state='disabled', command=lambda: self.pasteClipboard(None))
        self.pasteButton.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.pack(fill=tk.BOTH, expand=True)

        self.charWidth = 11
        self.lineHeight = 21

        self.focus_set()
        self.bind('<Key>', self.onKeyPress)
        self.bind('<Control-c>', self.copyselectionRange)
        self.bind('<Control-x>', self.cutselectionRange)
        self.bind('<Control-v>', self.pasteClipboard)
        self.bind('<Control-V>', self.pasteClipboardPop)
        self.bind('<Control-z>', self.obaviUndo)
        self.bind('<Control-y>', self.obaviRedo)

        cursor = self.model.getCursor()
        self.cursorX = self.charWidth * cursor.getColumn() + 5
        self.cursorY = cursor.getRow() * self.lineHeight + 10

        menu = tk.Menu(self.master) 

        fileMenu = tk.Menu(menu, tearoff=0)
        fileMenu.add_command(label='Open', command=self.openFile)
        fileMenu.add_command(label='Save', command=self.saveFile)
        fileMenu.add_command(label='Exit', command=self.closeWindow)
        menu.add_cascade(label='File', menu=fileMenu)

        editMenu = tk.Menu(menu, tearoff=0)
        editMenu.add_command(label='Undo', command=lambda: self.obaviUndo(None))
        editMenu.add_command(label='Redo', command=lambda: self.obaviRedo(None))
        editMenu.add_command(label='Cut', command=lambda: self.cutselectionRange(None))
        editMenu.add_command(label='Copy', command=lambda: self.copyselectionRange(None))
        editMenu.add_command(label='Paste', command=lambda: self.pasteClipboard(None))
        editMenu.add_command(label='Paste and Take', command=lambda: self.pasteClipboardPop(None))
        editMenu.add_command(label='Delete selection', command=self.deleteSelection)
        editMenu.add_command(label='Clear document', command=self.clearDocument)
        menu.add_cascade(label='Edit', menu=editMenu)

        moveMenu = tk.Menu(menu, tearoff=0)
        moveMenu.add_command(label='Cursor to document start', command=self.cursorStart)
        moveMenu.add_command(label='Cursor to document end', command=self.cursorEnd)
        menu.add_cascade(label='Move', menu=moveMenu)

        pluginsMenu = tk.Menu(menu, tearoff=0)
        plugins = getPlugins()
        for plugin in plugins:
            pluginsMenu.add_command(label=plugin.getName(), command=lambda p=plugin: p.execute(self.model, UndoManager.getInstance(), self.clipboard))
        menu.add_cascade(label='Plugins', menu=pluginsMenu)

        self.master.config(menu=menu) 

        self.draw()


    def doNothing(self):
        pass

    def openFile(self):
        file = filedialog.askopenfilename()
        if file and file.endswith('.txt'):
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                lines = self.model.getLines()
                row = len(lines) - 1
                column = len(lines[-1])
                self.model.deleteRange(LocationRange(Location(0, 0), Location(row, column)))
                self.model.insertText(text)

    def saveFile(self):
        file = filedialog.asksaveasfilename(defaultextension='.txt')
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                lines = self.model.getLines()
                f.write("\n".join(lines)) 

    def closeWindow(self):
        self.master.destroy()

    def deleteSelection(self):
        if self.model.getSelectionRange():
            self.model.deleteRange(self.model.getSelectionRange())
        
    def clearDocument(self):
        lines = self.model.getLines()
        row = len(lines) - 1
        column = len(lines[-1])
        self.model.deleteRange(LocationRange(Location(0, 0), Location(row, column)))
    
    def cursorStart(self):
        self.model.setCursorLocation(Location(0, 0))
    
    def cursorEnd(self):
        lines = self.model.getLines()
        row = len(lines) - 1
        column = len(lines[-1])
        self.model.setCursorLocation(Location(row, column))

    def draw(self):
        self.delete("all")

        selection = self.model.getSelectionRange()
        if selection:
            selStart, selEnd = selection.reverseIfNeeded()

        
        if self.index1 != 0 and self.index2 != 0:
            for i, line in enumerate(self.model.linesRange(self.index1, self.index2)):
                x = 5
                y = i * self.lineHeight + 10

                if selection and selStart.getRow() <= i and i <= selEnd.getRow():
                    if i == selStart.getRow():
                        startColumn = selStart.getColumn()
                    else:
                        startColumn = 0

                    if i == selEnd.getRow():
                        endColumn = selEnd.getColumn()
                    else:
                        endColumn = len(line)
                    x1 = startColumn * self.charWidth + 5
                    x2 = endColumn * self.charWidth + 5
                    self.create_rectangle(x1, y, x2, y + self.lineHeight, fill='lightblue', outline='')

                self.create_text(x, y, anchor='nw', text=line, font=('Courier New', 14), fill='black')
            
        else:
            for i, line in enumerate(self.model.allLines()):
                x = 5
                y = i * self.lineHeight + 10

                if selection and selStart.getRow() <= i and i <= selEnd.getRow():
                    if i == selStart.getRow():
                        startColumn = selStart.getColumn()
                    else:
                        startColumn = 0

                    if i == selEnd.getRow():
                        endColumn = selEnd.getColumn()
                    else:
                        endColumn = len(line)
                    x1 = startColumn * self.charWidth + 5
                    x2 = endColumn * self.charWidth + 5
                    self.create_rectangle(x1, y, x2, y + self.lineHeight, fill='lightblue', outline='')

                self.create_text(x, y, anchor='nw', text=line, font=('Courier New', 14), fill='black')
        
        self.create_line(self.cursorX, self.cursorY, self.cursorX, self.cursorY + self.lineHeight, fill='black')
        

    def updateCursorLocation(self, loc):
        self.cursorX = self.charWidth * loc.getColumn() + 5
        self.cursorY = loc.getRow() * self.lineHeight + 10
        self.draw()
    
    def updateText(self):
        if self.model.getSelectionRange():
            self.copyButton.config(state='normal')
            self.cutButton.config(state='normal')
        else:
            self.copyButton.config(state='disabled')
            self.cutButton.config(state='disabled')
        self.draw()

    def updateUndo(self, canUndo, canRedo):
        if canUndo:
            self.canUndo = True
            self.undoButton.config(state='normal')
        else:
            self.canUndo = False
            self.undoButton.config(state='disabled')

        if canRedo:
            self.canRedo = True
            self.redoButton.config(state='normal')
        else:
            self.canRedo = False
            self.redoButton.config(state='disabled')
    
    def updateClipboard(self):
        if not self.clipboard.isClipboardEmpty():
            self.pasteButton.config(state='normal')
        else:
            self.pasteButton.config(state='disabled')

    def onKeyPress(self, event):
        key = event.keysym

        if (event.state & 0x0001) != 0:
            if key == 'Left':
                if self.model.getSelectionRange() is None:
                    cursorLocationOld = self.model.getCursor()
                    self.model.moveCursorLeft()
                    self.model.setSelectionRange(LocationRange(cursorLocationOld, self.model.getCursor()))
                else:
                    selectionrange = self.model.getSelectionRange()
                    startRange = selectionrange.getStart()
                    self.model.moveCursorLeft()
                    self.model.setSelectionRange(LocationRange(startRange, self.model.getCursor()))
            elif key == 'Right':
                if self.model.getSelectionRange() is None:
                    cursorLocationOld = self.model.getCursor()
                    self.model.moveCursorRight()
                    self.model.setSelectionRange(LocationRange(cursorLocationOld, self.model.getCursor()))
                else:
                    selectionrange = self.model.getSelectionRange()
                    startRange = selectionrange.getStart()
                    self.model.moveCursorRight()
                    self.model.setSelectionRange(LocationRange(startRange, self.model.getCursor()))
            elif key == 'Up':
                if self.model.getSelectionRange() is None:
                    cursorLocationOld = self.model.getCursor()
                    self.model.moveCursorUp()
                    self.model.setSelectionRange(LocationRange(cursorLocationOld, self.model.getCursor()))
                else:
                    selectionrange = self.model.getSelectionRange()
                    startRange = selectionrange.getStart()
                    self.model.moveCursorUp()
                    self.model.setSelectionRange(LocationRange(startRange, self.model.getCursor()))
            elif key == 'Down':
                if self.model.getSelectionRange() is None:
                    cursorLocationOld = self.model.getCursor()
                    self.model.moveCursorDown()
                    self.model.setSelectionRange(LocationRange(cursorLocationOld, self.model.getCursor()))
                else:
                    selectionrange = self.model.getSelectionRange()
                    startRange = selectionrange.getStart()
                    self.model.moveCursorDown()
                    self.model.setSelectionRange(LocationRange(startRange, self.model.getCursor()))
            elif key == 'BackSpace':
                if self.model.getSelectionRange():
                    self.model.deleteRange(self.model.getSelectionRange())
                else:
                    self.model.deleteBefore()
            elif key == 'Delete':
                if self.model.getSelectionRange():
                    self.model.deleteRange(self.model.getSelectionRange())
                else:
                    self.model.deleteAfter()
            elif len(event.char) == 1 and ord(event.char) >= 32:
                self.model.insert(event.char)
            elif key == 'Return':
                self.model.insert('\n')
            
        else:
            if event.keysym == 'Left':
                self.model.moveCursorLeft()
            elif event.keysym == 'Right':
                self.model.moveCursorRight()
            elif event.keysym == 'Up':
                self.model.moveCursorUp()
            elif event.keysym == 'Down':
                self.model.moveCursorDown()
            elif key == 'BackSpace':
                if self.model.getSelectionRange():
                    self.model.deleteRange(self.model.getSelectionRange())
                else:
                    self.model.deleteBefore()
            elif key == 'Delete':
                if self.model.getSelectionRange():
                    self.model.deleteRange(self.model.getSelectionRange())
                else:
                    self.model.deleteAfter()
            elif len(event.char) == 1 and ord(event.char) >= 32:
                self.model.insert(event.char)
            elif key == 'Return':
                self.model.insert('\n')


        self.draw()

    def copyselectionRange(self, event):
        selection = self.model.getSelectionRange()
        if self.model.getSelectionRange():
            start, end = selection.reverseIfNeeded()
            oznText = []
            for r in range(start.getRow(), end.getRow() + 1):
                line = self.model.lines[r]
                if r == start.getRow():
                    startIndex = start.getColumn()
                else:
                    startIndex = 0
                if r == end.getRow():
                    endIndex = end.getColumn()
                else:
                    endIndex = len(line)
                oznText.append(line[startIndex:endIndex])
            copiranText = "\n".join(oznText)
            self.clipboard.addToClipboard(copiranText)

    def cutselectionRange(self, event):
        selection = self.model.getSelectionRange()
        if selection:
            self.copyselectionRange(event)
            self.model.deleteRange(selection)

    def pasteClipboard(self, event):
        if not self.clipboard.isClipboardEmpty():
            text = self.clipboard.topOfClipboard()
            self.model.insertText(text)

    def pasteClipboardPop(self, event):
        if not self.clipboard.isClipboardEmpty():
            text = self.clipboard.removeFromClipboard()
            self.model.insertText(text)

    def obaviUndo(self, event):
        if self.canUndo:
            UndoManager.getInstance().undo()

    def obaviRedo(self, event):
        if self.canRedo:
            UndoManager.getInstance().redo()