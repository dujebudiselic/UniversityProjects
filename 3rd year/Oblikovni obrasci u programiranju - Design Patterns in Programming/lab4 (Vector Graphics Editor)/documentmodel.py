from listeners import GraphicalObjectListener

class DocumentModel(GraphicalObjectListener):
    SELECTION_PROXIMITY = 10

    def __init__(self):
        self.objects = []
        self.roObjects = tuple(self.objects)
        self.listeners = []
        self.selectedObjects = []
        self.roSelectedObjects = tuple(self.selectedObjects)


    def clear(self):
        for o in self.objects:
            o.removeGraphicalObjectListener(self)
        self.objects.clear()
        self.selectedObjects.clear()
        self.roObjects = tuple(self.objects)
        self.roSelectedObjects = tuple(self.selectedObjects)
        self.notifyListeners()

    def addGraphicalObject(self, obj):
        if obj.isSelected() and obj not in self.selectedObjects:
            self.selectedObjects.append(obj)
        self.objects.append(obj)
        self.roObjects = tuple(self.objects)
        self.roSelectedObjects = tuple(self.selectedObjects)
        obj.addGraphicalObjectListener(self)
        self.notifyListeners()

    def removeGraphicalObject(self, obj):
        if obj in self.objects:
            if obj in self.selectedObjects:
                obj.setSelected(False)
            self.objects.remove(obj)
            self.roObjects = tuple(self.objects)
            self.roSelectedObjects = tuple(self.selectedObjects)
            obj.removeGraphicalObjectListener(self)
            self.notifyListeners()

    def list(self):
        return tuple(self.objects)

    def addDocumentModelListener(self, l):
        self.listeners.append(l)

    def removeDocumentModelListener(self, l):
        if l in self.listeners:
            self.listeners.remove(l)

    def notifyListeners(self):
        for l in self.listeners:
            l.documentChange()

    def getSelectedObjects(self):
        return tuple(self.selectedObjects)

    def increaseZ(self, go):
        index = self.objects.index(go)
        if index < len(self.objects) - 1:
            self.objects[index], self.objects[index + 1] = self.objects[index + 1], self.objects[index]
            self.roObjects = tuple(self.objects)
            self.notifyListeners()

    def decreaseZ(self, go):
        index = self.objects.index(go)
        if index > 0:
            self.objects[index], self.objects[index - 1] = self.objects[index - 1], self.objects[index]
            self.roObjects = tuple(self.objects)
            self.notifyListeners()

    def findSelectedGraphicalObject(self, mousePoint):
        closest = None
        minDis = self.SELECTION_PROXIMITY
        for o in self.objects: 
            dis = o.selectionDistance(mousePoint)
            if dis <= minDis:
                minDis = dis
                closest = o
        if closest:
            return closest
        else: 
            return None

    def findSelectedHotPoint(self, obj, mousePoint):
        index = -1
        minDis = self.SELECTION_PROXIMITY
        numHotPoints = obj.getNumberOfHotPoints()
        for i in range(numHotPoints):
            dis = obj.getHotPointDistance(i, mousePoint)
            if dis <= minDis:
                minDis = dis
                index = i
        if index != -1:    
            return index
        else:
            return -1
        
    def graphicalObjectChanged(self, go):
        self.notifyListeners()

    def graphicalObjectSelectionChanged(self, go):
        if go.isSelected():
            if go not in self.selectedObjects:
                self.selectedObjects.append(go)
            self.roSelectedObjects = tuple(self.selectedObjects)
        else:
            if go in self.selectedObjects:
                self.selectedObjects.remove(go)
            self.roSelectedObjects = tuple(self.selectedObjects)
        self.notifyListeners()