from location import Location, LocationRange
from undomanager import UndoManager
from commands import DeleteAction, InsertCharAction, InsertTextAction

class TextEditorModel:
    def __init__(self, text):
        self.lines = text.split('\n')
        self.cursorLocation = Location(0, 0)
        self.selectionRange = None 
        self.cursorObservers = []
        self.textObservers = []

    def getLines(self):
        return self.lines
    
    def getSelectionRange(self):
        return self.selectionRange

    def setSelectionRange(self, range):
        self.selectionRange = range
        self.notifyTextObservers()
    
    def setCursorLocation(self, c):
        self.cursorLocation = c
        self.notifyCursorObservers()

    def getCursor(self):
        return self.cursorLocation
    
    def allLines(self):
        return iter(self.lines)

    def linesRange(self, index1, index2):
        linesRange = []
        while index1 < index2:
            linesRange.append(self.lines[index1-1])
            index1 = index1 + 1
        return iter(linesRange)

    def addCursorObserver(self, o):
        self.cursorObservers.append(o)
        self.notifyCursorObservers()

    def addTextObserver(self, o):
        self.textObservers.append(o)
        self.notifyTextObservers()

    def removeCursorObserver(self, o):
        if o in self.cursorObservers:
            self.cursorObservers.remove(o)

    def removeTextObserver(self, o):
        if o in self.textObservers:
            self.textObservers.remove(o)

    def notifyCursorObservers(self):
        for p in self.cursorObservers:
            p.updateCursorLocation(self.cursorLocation)

    def notifyTextObservers(self):
        for p in self.textObservers:
            p.updateText()

    def moveCursorLeft(self):
        if self.cursorLocation.getColumn() > 0:
            self.cursorLocation = Location(self.cursorLocation.getRow(), self.cursorLocation.getColumn() - 1)
        elif self.cursorLocation.getColumn() == 0 and self.cursorLocation.getRow() > 0:
            lineBefore = len(self.lines[self.cursorLocation.getRow() - 1])
            self.cursorLocation = Location(self.cursorLocation.getRow() - 1, lineBefore)
        self.setSelectionRange(None)
        self.notifyCursorObservers()

    def moveCursorRight(self):
        lineLen = len(self.lines[self.cursorLocation.getRow()])
        if self.cursorLocation.getColumn() < lineLen:
            self.cursorLocation = Location(self.cursorLocation.getRow(), self.cursorLocation.getColumn() + 1)
        elif self.cursorLocation.getColumn() == lineLen and self.cursorLocation.getRow() < len(self.lines) - 1:
            self.cursorLocation = Location(self.cursorLocation.getRow() + 1, 0)
        self.setSelectionRange(None)
        self.notifyCursorObservers()


    def moveCursorUp(self):
        if self.cursorLocation.getRow() > 0:
            rowUp = self.cursorLocation.getRow() - 1
            if self.cursorLocation.getColumn() < len(self.lines[rowUp]):
                columnUp = self.cursorLocation.getColumn()
            else:
                columnUp = len(self.lines[rowUp])
            self.cursorLocation = Location(rowUp, columnUp)
            self.setSelectionRange(None)
            self.notifyCursorObservers()


    def moveCursorDown(self):
        if self.cursorLocation.getRow() < len(self.lines) - 1:
            rowDown = self.cursorLocation.getRow() + 1
            if self.cursorLocation.getColumn() < len(self.lines[rowDown]):
                columnDown = self.cursorLocation.getColumn()
            else:
                columnDown = len(self.lines[rowDown])
            self.cursorLocation = Location(rowDown, columnDown)
            self.setSelectionRange(None)
            self.notifyCursorObservers()

    def deleteBefore(self, noRepeatAction=True):
        loc = self.cursorLocation
        if loc.getColumn() == 0 and loc.getRow() > 0:
            lineBefore = self.lines[loc.getRow() - 1]
            lineAfter = self.lines.pop(loc.getRow())
            self.lines[loc.getRow() - 1] = self.lines[loc.getRow() - 1] + lineAfter 
            self.cursorLocation = Location(loc.getRow() - 1, len(lineBefore))
            if noRepeatAction:
                UndoManager.getInstance().push(DeleteAction(self, Location(loc.getRow() - 1, len(lineBefore)), '\n', None, 'before', 'newLine'))
        elif loc.getColumn() > 0:
            line = self.lines[loc.getRow()]
            charDeleted = line[loc.getColumn() - 1]
            self.lines[loc.getRow()] = line[:loc.getColumn() - 1] + line[loc.getColumn():]
            self.cursorLocation = Location(loc.getRow(), loc.getColumn() - 1)
            if noRepeatAction:
                UndoManager.getInstance().push(DeleteAction(self, Location(loc.getRow(), loc.getColumn() - 1), charDeleted, None, 'before'))

        self.setSelectionRange(None)
        self.notifyTextObservers()
        self.notifyCursorObservers()

    def deleteAfter(self, noRepeatAction=True):
        loc = self.cursorLocation
        line = self.lines[loc.getRow()]
        if loc.getColumn() < len(line):
            charDeleted = line[loc.getColumn()]
            if noRepeatAction:
                UndoManager.getInstance().push(DeleteAction(self, Location(self.cursorLocation.getRow(), self.cursorLocation.getColumn()), charDeleted, None, 'after'))
            self.lines[loc.getRow()] = line[:loc.getColumn()] + line[loc.getColumn() + 1:]
        elif loc.getColumn() == len(line) and loc.getRow() < len(self.lines) - 1:
            if noRepeatAction:
                UndoManager.getInstance().push(DeleteAction(self, Location(self.cursorLocation.getRow(), self.cursorLocation.getColumn()), '\n', None, 'after', 'newLine'))
            lineAfter = self.lines.pop(loc.getRow() + 1)
            self.lines[loc.getRow()] = self.lines[loc.getRow()] + lineAfter
        self.setSelectionRange(None)
        self.notifyTextObservers()
        self.notifyCursorObservers()

    def deleteRange(self, r, noRepeatAction=True):
        start, end = r.reverseIfNeeded()
        
        delText = []
        for r in range(start.getRow(), end.getRow() + 1):
            line = self.lines[r]
            if r == start.getRow():
                startIndex = start.getColumn()
            else:
                startIndex = 0
            if r == end.getRow():
                endIndex = end.getColumn()
            else:
                endIndex = len(line)
            delText.append(line[startIndex:endIndex])
        deletedText = "\n".join(delText)

        if start.getRow() == end.getRow():
            line = self.lines[start.getRow()]
            self.lines[start.getRow()] = line[:start.getColumn()] + line[end.getColumn():]
        else:
            startLine = self.lines[start.getRow()]
            endLine = self.lines[end.getRow()]
            beforeDeleted = startLine[:start.getColumn()]
            afterDeleted = endLine[end.getColumn():]
            del self.lines[start.getRow():end.getRow() + 1]
            self.lines.insert(start.getRow(), beforeDeleted + afterDeleted)
        self.cursorLocation = Location(start.getRow(), start.getColumn())
        if noRepeatAction:
            UndoManager.getInstance().push(DeleteAction(self, Location(start.getRow(), start.getColumn()), deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn())), 'before'))
        self.setSelectionRange(None)
        self.notifyTextObservers()
        self.notifyCursorObservers()


    def insert(self, c, direction = None, noRepeatAction=True):
        sR = False
        if self.selectionRange:
            sR = True
            start, end = self.selectionRange.reverseIfNeeded()
            delText = []
            for r in range(start.getRow(), end.getRow() + 1):
                line = self.lines[r]
                if r == start.getRow():
                    startIndex = start.getColumn()
                else:
                    startIndex = 0
                if r == end.getRow():
                    endIndex = end.getColumn()
                else:
                    endIndex = len(line)
                delText.append(line[startIndex:endIndex])
            deletedText = "\n".join(delText)
            self.deleteRange(self.selectionRange, noRepeatAction=False)
        
        loc = self.cursorLocation
        line = self.lines[loc.getRow()]
        if c == '\n':
            lineBefore = line[:loc.getColumn()]
            lineAfter = line[loc.getColumn():]
            self.lines[loc.getRow()] = lineBefore
            self.lines.insert(loc.getRow() + 1, lineAfter)
            if direction == 'after':
                self.cursorLocation = Location(loc.getRow(), loc.getColumn())
            else:
                self.cursorLocation = Location(loc.getRow() + 1, 0)
                if noRepeatAction:
                    if sR:
                        UndoManager.getInstance().push(InsertCharAction(self, Location(loc.getRow() + 1, 0), c, deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn()))))
                    else:
                        UndoManager.getInstance().push(InsertCharAction(self, Location(loc.getRow() + 1, 0), c))
        else:
            self.lines[loc.getRow()] = line[:loc.getColumn()] + c + line[loc.getColumn():]
            if direction == 'after':
                self.cursorLocation = Location(loc.getRow(), loc.getColumn())
            else:
                self.cursorLocation = Location(loc.getRow(), loc.getColumn() + 1)
                if noRepeatAction:
                    if sR:
                        UndoManager.getInstance().push(InsertCharAction(self, Location(loc.getRow(), loc.getColumn() + 1), c, deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn()))))
                    else:
                        UndoManager.getInstance().push(InsertCharAction(self, Location(loc.getRow(), loc.getColumn() + 1), c))

        self.setSelectionRange(None)
        self.notifyTextObservers()
        self.notifyCursorObservers()

    def insertText(self, text, direction = None, noRepeatAction=True):
        sR = False
        if self.selectionRange:
            sR = True
            start, end = self.selectionRange.reverseIfNeeded()
            delText = []
            for r in range(start.getRow(), end.getRow() + 1):
                line = self.lines[r]
                if r == start.getRow():
                    startIndex = start.getColumn()
                else:
                    startIndex = 0
                if r == end.getRow():
                    endIndex = end.getColumn()
                else:
                    endIndex = len(line)
                delText.append(line[startIndex:endIndex])
            deletedText = "\n".join(delText)
            self.deleteRange(self.selectionRange, noRepeatAction=False)

        loc = self.cursorLocation
        textLines = text.split('\n')
        cursorLocationOld = self.getCursor()

        if len(textLines) == 1:
            line = self.lines[loc.getRow()]
            self.lines[loc.getRow()] = line[:loc.getColumn()] + textLines[0] + line[loc.getColumn():]
            if direction == 'after':
                self.cursorLocation = Location(loc.getRow(), loc.getColumn())
                if noRepeatAction:
                    if sR:
                        UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow(), loc.getColumn()), text, deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn()))))
                    else:
                        UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow(), loc.getColumn()), text))
            else:
                self.cursorLocation = Location(loc.getRow(), loc.getColumn() + len(textLines[0]))
                if noRepeatAction:
                    if sR:
                        UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow(), loc.getColumn() + len(textLines[0])), text, deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn()))))
                    else:
                        UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow(), loc.getColumn() + len(textLines[0])), text))
        else:
            line = self.lines[loc.getRow()]
            lineBefore = line[:loc.getColumn()]
            lineAfter = line[loc.getColumn():]
            linesIzmedu = textLines[1:-1]
            self.lines[loc.getRow()] = lineBefore + textLines[0]
            i = 1
            for l in linesIzmedu:
                self.lines.insert(loc.getRow() + i, l)
                i += 1
            self.lines.insert(loc.getRow() + i, textLines[-1] + lineAfter)
            self.cursorLocation = Location(loc.getRow() + len(textLines) - 1, len(textLines[-1])) 
            if noRepeatAction:
                if sR:
                    UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow() + len(textLines) - 1, len(textLines[-1])), text, deletedText, LocationRange(Location(start.getRow(), start.getColumn()), Location(end.getRow(), end.getColumn()))))
                else:
                    UndoManager.getInstance().push(InsertTextAction(self, cursorLocationOld, Location(loc.getRow() + len(textLines) - 1, len(textLines[-1])), text))


        self.setSelectionRange(None)
        self.notifyTextObservers()
        self.notifyCursorObservers()