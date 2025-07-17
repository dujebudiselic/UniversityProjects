from abc import ABC, abstractmethod
from location import Location, LocationRange

class EditAction(ABC):
    @abstractmethod
    def execute_do(self):
        pass

    @abstractmethod
    def execute_undo(self):
        pass

class InsertCharAction(EditAction):
    def __init__(self, model, cursorLocAfter, char, deletedText = '', selRange = None):
        self.model = model
        self.cursorLocAfter = cursorLocAfter 
        self.char = char
        self.deletedText = deletedText
        self.selRange = selRange

    def execute_do(self):
        if self.model.getCursor() != self.cursorLocAfter:
            self.model.setCursorLocation(Location(self.cursorLocAfter.getRow(), self.cursorLocAfter.getColumn() - 1))
        if self.selRange is not None:
            self.model.deleteRange(self.selRange, noRepeatAction=False)
        self.model.insert(self.char, noRepeatAction=False)

    def execute_undo(self):
        if self.model.getCursor() != self.cursorLocAfter:
            self.model.setCursorLocation(self.cursorLocAfter)
        self.model.deleteBefore(noRepeatAction=False)
        if self.deletedText != '':
            self.model.insertText(self.deletedText, noRepeatAction=False)


class InsertTextAction(EditAction):
    def __init__(self, model, cursorLocationOld, cursorLocAfter, text, deletedText='', selRange = None):
        self.model = model
        self.cursorLocationOld = cursorLocationOld
        self.cursorLocAfter = cursorLocAfter
        self.text = text
        self.deletedText = deletedText
        self.selRange = selRange

    def execute_do(self):
        if self.selRange:
            self.model.deleteRange(self.selRange, noRepeatAction=False)
        else:
            self.model.setCursorLocation(self.cursorLocationOld)
        self.model.insertText(self.text, noRepeatAction=False)

    def execute_undo(self):
        if self.selRange:
            rangeText = LocationRange(Location(self.selRange.getStart().getRow(), self.selRange.getStart().getColumn()), self.cursorLocAfter)
        else:
            rangeText = LocationRange(self.cursorLocationOld, self.cursorLocAfter)
        self.model.deleteRange(rangeText, noRepeatAction=False)
        if self.selRange:
            self.model.insertText(self.deletedText, noRepeatAction=False)

class DeleteAction(EditAction):
    def __init__(self, model, cursorLocAfter, text, selRange = None, direction = None, newLine = ''):
        self.model = model
        self.cursorLocAfter = cursorLocAfter 
        self.text = text
        self.selRange = selRange
        self.direction = direction
        self.newLine = newLine

    def execute_do(self):
        if self.selRange is not None:
            self.model.deleteRange(self.selRange, noRepeatAction=False)
        else:
            if self.direction == 'before':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(Location(self.cursorLocAfter.getRow(), self.cursorLocAfter.getColumn() + 1))
                if self.newLine != '':
                    self.model.setCursorLocation(Location(self.cursorLocAfter.getRow() + 1, 0))
                self.model.deleteBefore(noRepeatAction=False)

            elif self.direction == 'after':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(self.cursorLocAfter)
                self.model.deleteAfter(noRepeatAction=False)

    def execute_undo(self):
        if self.selRange is not None:
            if self.direction == 'before':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(self.cursorLocAfter)
                self.model.insertText(self.text, noRepeatAction=False)

            elif self.direction == 'after':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(self.cursorLocAfter)
                self.model.insertText(self.text, self.direction, noRepeatAction=False)
        else:
            if self.direction == 'before':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(self.cursorLocAfter)
                self.model.insert(self.text, noRepeatAction=False)

            elif self.direction == 'after':
                if self.model.getCursor() != self.cursorLocAfter:
                    self.model.setCursorLocation(self.cursorLocAfter)
                self.model.insert(self.text, self.direction, noRepeatAction=False)