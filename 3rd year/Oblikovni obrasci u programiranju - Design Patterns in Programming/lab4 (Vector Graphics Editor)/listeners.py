from abc import ABC, abstractmethod

class GraphicalObjectListener(ABC):

    @abstractmethod
    def graphicalObjectChanged(self, go):
        pass

    @abstractmethod
    def graphicalObjectSelectionChanged(self, go):
        pass

class DocumentModelListener(ABC):

    @abstractmethod
    def documentChange(self):
        pass