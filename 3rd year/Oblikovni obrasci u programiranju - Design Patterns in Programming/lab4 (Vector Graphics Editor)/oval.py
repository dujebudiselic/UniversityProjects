from abstractgraphicalobject import AbstractGraphicalObject
from pointrectangle import Point, Rectangle
from geometryutil import GeometryUtil
import math

class Oval(AbstractGraphicalObject):
    def __init__(self, rightHotPoint=None, bottomHotPoint=None):
        if rightHotPoint is None and bottomHotPoint is None:
            rightHotPoint = Point(10, 0)
            bottomHotPoint = Point(0, 10)
        hotPoints = [rightHotPoint, bottomHotPoint]
        super().__init__(hotPoints)

    def selectionDistance(self, mousePoint):
        cX = self.hotPoints[1].getX()  
        cY = self.hotPoints[0].getY()  

        rX = abs(self.hotPoints[0].getX() - cX)
        rY = abs(self.hotPoints[1].getY() - cY)

        mPX, mPY = mousePoint.getX(), mousePoint.getY()

        nX = (mPX - cX) / rX
        nY = (mPY - cY) / rY

        if nX**2 + nY**2 <= 1:
            return 0
        else:
            t = math.atan2(nY, nX)
            x = cX + rX * math.cos(t)
            y = cY + rY * math.sin(t)
            return GeometryUtil.distanceFromPoint(mousePoint, Point(x, y))

    def getBoundingBox(self):
        cX = self.hotPoints[1].getX()
        cY = self.hotPoints[0].getY()

        rX = abs(self.hotPoints[0].getX() - cX)
        rY = abs(self.hotPoints[1].getY() - cY)

        x = cX - rX
        y = cY - rY
        width = 2 * rX
        height = 2 * rY

        return Rectangle(x, y, width, height)

    def duplicate(self):
        hP1 = self.hotPoints[0]
        hP2 = self.hotPoints[1]
        return Oval(Point(hP1.getX(), hP1.getY()), Point(hP2.getX(), hP2.getY()))

    def getShapeName(self):
        return 'Oval'
    
    def render(self, r):
        cX = self.hotPoints[1].getX()
        cY = self.hotPoints[0].getY()

        rX = abs(self.hotPoints[0].getX() - cX)
        rY = abs(self.hotPoints[1].getY() - cY)

        points = []
        for i in range(180): 
            angle = 2 * math.pi * i / 180
            x = cX + rX * math.cos(angle) + 0.5 
            y = cY + rY * math.sin(angle) + 0.5
            points.append(Point(int(x), int(y)))
        
        if self.isSelected():
            r.fillPolygon(points, 'red')
        else:
            r.fillPolygon(points, 'blue')