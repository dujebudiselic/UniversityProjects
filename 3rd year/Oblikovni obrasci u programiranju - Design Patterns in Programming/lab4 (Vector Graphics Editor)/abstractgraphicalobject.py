from graphicalobject import GraphicalObject
from geometryutil import GeometryUtil

class AbstractGraphicalObject(GraphicalObject):
    def __init__(self, hotPoints):
        self.hotPoints = hotPoints
        self.hotPointSelected = []
        for i in range(len(hotPoints)):
            self.hotPointSelected.append(False)
        self.selected = False
        self.listeners = []

    def getHotPoint(self, index):
        return self.hotPoints[index]

    def setHotPoint(self, index, point):
        self.hotPoints[index] = point
        self.notifyListeners()

    def getNumberOfHotPoints(self):
        return len(self.hotPoints)

    def getHotPointDistance(self, index, mousePoint):
        return GeometryUtil.distanceFromPoint(self.hotPoints[index], mousePoint)

    def isHotPointSelected(self, index):
        return self.hotPointSelected[index]

    def setHotPointSelected(self, index, selected):
        self.hotPointSelected[index] = selected
        self.notifyListeners()

    def isSelected(self):
        return self.selected

    def setSelected(self, selected):
        self.selected = selected
        self.notifySelectionListeners()

    def translate(self, delta):
        translatedPoints = []
        for p in self.hotPoints:
            translatedPoints.append(p.translate(delta))
        self.hotPoints = translatedPoints
        self.notifyListeners()

    def addGraphicalObjectListener(self, l):
        self.listeners.append(l)

    def removeGraphicalObjectListener(self, l):
        if l in self.listeners:
            self.listeners.remove(l)

    def notifyListeners(self):
        for l in self.listeners:
            l.graphicalObjectChanged(self)

    def notifySelectionListeners(self):
        for l in self.listeners:
            l.graphicalObjectSelectionChanged(self)