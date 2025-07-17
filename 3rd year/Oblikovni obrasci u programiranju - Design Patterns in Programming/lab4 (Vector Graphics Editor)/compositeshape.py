from graphicalobject import GraphicalObject
from pointrectangle import Rectangle

class CompositeShape(GraphicalObject):
    def __init__(self, listGO = None):
        if listGO:
            self.listGO = listGO
        else:
            self.listGO = []
        self.selected = False
        self.listeners = []

    def GetlistGO(self):
        return self.listGO

    def addGraphicalObject(self, go):
        self.listGO.append(go)
        self.notifyListeners()
    
    def isSelected(self):
        return self.selected

    def setSelected(self, selected):
        self.selected = selected
        self.notifySelectionListeners()

    def getNumberOfHotPoints(self):
        return 0

    def getHotPoint(self, index):
        pass

    def setHotPoint(self, index, point):
        pass

    def isHotPointSelected(self, index):
        pass

    def setHotPointSelected(self, index, selected):
        pass

    def getHotPointDistance(self, index, mousePoint):
        pass

    def translate(self, delta):
        for o in self.listGO:
            o.translate(delta)
        self.notifyListeners()

    def getBoundingBox(self):
        boundingBox = self.listGO[0].getBoundingBox()
        minX = boundingBox.getX()
        minY = boundingBox.getY()
        maxX = minX + boundingBox.getWidth()
        maxY = minY + boundingBox.getHeight()

        for o in self.listGO[1:]:
            boundingBox = o.getBoundingBox()
            if boundingBox.getX() < minX:
                minX = boundingBox.getX()
            if boundingBox.getY() < minY:
                minY = boundingBox.getY()
            if boundingBox.getX() + boundingBox.getWidth() > maxX:
                maxX = boundingBox.getX() + boundingBox.getWidth()
            if boundingBox.getY() + boundingBox.getHeight() > maxY:
                maxY = boundingBox.getY() + boundingBox.getHeight()
        width = maxX - minX
        height = maxY - minY
        return Rectangle(minX, minY, width, height)

    def selectionDistance(self, mousePoint):
        minDis = float('inf')
        for o in self.listGO:
            dis = o.selectionDistance(mousePoint)
            if dis < minDis:
                minDis = dis
        return minDis

    def render(self, r):
        for o in self.listGO:
            o.render(r)

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

    def getShapeName(self):
        return 'CompositeShape'

    def duplicate(self):
        dup = []
        for o in self.listGO:
            dupGo = o.duplicate()
            dup.append(dupGo)
        return CompositeShape(dup)