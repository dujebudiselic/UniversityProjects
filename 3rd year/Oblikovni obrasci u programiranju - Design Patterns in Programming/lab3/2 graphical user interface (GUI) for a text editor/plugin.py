from abc import ABC, abstractmethod

class plugin(ABC):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getDescription(self):
        pass

    @abstractmethod
    def execute(self, model, undoManager, clipboardStack):
        pass
