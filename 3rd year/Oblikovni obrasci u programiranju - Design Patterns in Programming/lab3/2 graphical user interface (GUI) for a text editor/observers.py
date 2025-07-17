from abc import ABC, abstractmethod

class CursorObserver(ABC):
    @abstractmethod
    def updateCursorLocation(self, loc):
        pass

class TextObserver(ABC):
    @abstractmethod
    def updateText(self):
        pass

class ClipboardObserver(ABC):
    @abstractmethod
    def updateClipboard(self):
        pass

class UndoObserver(ABC):
    @abstractmethod
    def updateUndo(self, canUndo, canRedo):
        pass