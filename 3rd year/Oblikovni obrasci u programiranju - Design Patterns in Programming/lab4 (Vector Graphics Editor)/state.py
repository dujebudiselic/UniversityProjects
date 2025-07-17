from abc import ABC, abstractmethod
from compositeshape import CompositeShape
from pointrectangle import Point

class State(ABC):
    @abstractmethod
    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        pass

    @abstractmethod
    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        pass

    @abstractmethod
    def mouseDragged(self, mousePoint):
        pass

    @abstractmethod
    def keyPressed(self, keyCode):
        pass

    @abstractmethod
    def afterDraw(self, r, go):
        pass

    @abstractmethod
    def afterDraw_(self, r):
        pass

    @abstractmethod
    def onLeaving(self):
        pass

class IdleState(State):
    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        pass

    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        pass

    def mouseDragged(self, mousePoint):
        pass

    def keyPressed(self, keyCode):
        pass

    def afterDraw(self, r, go):
        pass

    def afterDraw_(self, r):
        pass

    def onLeaving(self):
        pass

class AddShapeState(State):
    def __init__(self, model, prototype):
        self.model = model
        self.prototype = prototype

    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        newObj = self.prototype.duplicate()
        newObj.translate(mousePoint)
        self.model.addGraphicalObject(newObj)

    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        pass

    def mouseDragged(self, mousePoint):
        pass

    def keyPressed(self, keyCode):
        pass

    def afterDraw(self, r, go):
        pass

    def afterDraw_(self, r):
        pass

    def onLeaving(self):
        pass

class SelectShapeState(State):
    def __init__(self, model):
        self.model = model

    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        selectObj = self.model.findSelectedGraphicalObject(mousePoint)
        if selectObj is None:
            for o in self.model.getSelectedObjects()[:]:
                o.setSelected(False)
        else:
            if ctrlDown:
                if selectObj in self.model.getSelectedObjects():
                    selectObj.setSelected(False)
                else:
                    selectObj.setSelected(True)
            else:
                for o in self.model.getSelectedObjects()[:]:
                    o.setSelected(False)
                selectObj.setSelected(True)

    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        pass

    def mouseDragged(self, mousePoint):
        obj = self.model.getSelectedObjects()[0]
        index = self.model.findSelectedHotPoint(obj, mousePoint)
        obj.setHotPoint(index, mousePoint)

    def keyPressed(self, keyCode):
        if keyCode == 38:  
            for o in self.model.getSelectedObjects():
                o.translate(Point(0,-1))
        elif keyCode == 40:  
            for o in self.model.getSelectedObjects():
                o.translate(Point(0,1))
        elif keyCode == 37:  
            for o in self.model.getSelectedObjects():
                o.translate(Point(-1,0))
        elif keyCode == 39:  
            for o in self.model.getSelectedObjects():
                o.translate(Point(1,0))
        elif keyCode == 107 and len(self.model.getSelectedObjects()) == 1:
            obj = self.model.getSelectedObjects()[0] 
            self.model.increaseZ(obj)
        elif keyCode == 109 and len(self.model.getSelectedObjects()) == 1:
            obj = self.model.getSelectedObjects()[0]
            self.model.decreaseZ(obj)
        elif keyCode == 71:
            if len(self.model.getSelectedObjects()) > 1:
                groupObj = list(self.model.getSelectedObjects())   
                composite = CompositeShape(groupObj)
                composite.setSelected(True)
                
                for o in groupObj:
                    self.model.removeGraphicalObject(o)
                
                self.model.addGraphicalObject(composite)
        
        elif keyCode == 85 and len(self.model.getSelectedObjects()) == 1 and isinstance(self.model.getSelectedObjects()[0], CompositeShape):
            compositeShape = self.model.getSelectedObjects()[0]
            originalObj = compositeShape.GetlistGO()
            compositeShape.setSelected(False)
            self.model.removeGraphicalObject(compositeShape)
            
            for o in originalObj:
                o.setSelected(True)
                self.model.addGraphicalObject(o)

    def afterDraw(self, r, go):
        if go.isSelected():
            boundingBox = go.getBoundingBox()
            x = boundingBox.getX()
            y = boundingBox.getY()
            width = boundingBox.getWidth()
            height = boundingBox.getHeight()
            r.drawLine(Point(x, y), Point(x + width, y), 'blue')
            r.drawLine(Point(x + width, y), Point(x + width, y + height), 'blue')
            r.drawLine(Point(x + width, y + height), Point(x, y + height), 'blue')
            r.drawLine(Point(x, y), Point(x, y + height), 'blue')
        if len(self.model.getSelectedObjects()) == 1 and go.isSelected():
            for i in range(go.getNumberOfHotPoints()):
                hotPoint = go.getHotPoint(i)
                x = hotPoint.getX()
                y = hotPoint.getY()
                x = x - 2
                y = y - 2
                r.drawLine(Point(x, y), Point(x + 5, y), 'blue')
                r.drawLine(Point(x + 5, y), Point(x + 5, y + 5), 'blue')
                r.drawLine(Point(x + 5, y + 5), Point(x, y + 5), 'blue')
                r.drawLine(Point(x, y), Point(x, y + 5), 'blue')

    def afterDraw_(self, r):
        pass

    def onLeaving(self):
        for o in self.model.getSelectedObjects(): 
            o.setSelected(False)
        self.model.notifyListeners()