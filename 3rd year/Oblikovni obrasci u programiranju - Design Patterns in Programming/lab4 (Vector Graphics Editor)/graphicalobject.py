from abc import ABC, abstractmethod

class GraphicalObject(ABC):

    @abstractmethod
    def isSelected(self):
        pass

    @abstractmethod
    def setSelected(self, selected):
        pass

    @abstractmethod
    def getNumberOfHotPoints(self):
        pass

    @abstractmethod
    def getHotPoint(self, index):
        pass

    @abstractmethod
    def setHotPoint(self, index, point):
        pass

    @abstractmethod
    def isHotPointSelected(self, index):
        pass

    @abstractmethod
    def setHotPointSelected(self, index, selected):
        pass

    @abstractmethod
    def getHotPointDistance(self, index, mousePoint):
        pass

    @abstractmethod
    def translate(self, delta):
        pass

    @abstractmethod
    def getBoundingBox(self):
        pass

    @abstractmethod
    def selectionDistance(self, mousePoint):
        pass

    @abstractmethod
    def render(self, r):
        pass

    @abstractmethod
    def addGraphicalObjectListener(self, l):
        pass

    @abstractmethod
    def removeGraphicalObjectListener(self, l):
        pass

    @abstractmethod
    def getShapeName(self):
        pass

    @abstractmethod
    def duplicate(self):
        pass