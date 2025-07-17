from abstractgraphicalobject import AbstractGraphicalObject
from pointrectangle import Point, Rectangle
from geometryutil import GeometryUtil

class LineSegment(AbstractGraphicalObject):
    def __init__(self, startPoint=None, endPoint=None):
        if startPoint is None and endPoint is None:
            startPoint = Point(0, 0)
            endPoint = Point(10, 0)
        hotPoints = [startPoint, endPoint]
        super().__init__(hotPoints)

    def selectionDistance(self, mousePoint):
        return GeometryUtil.distanceFromLineSegment(self.hotPoints[0], self.hotPoints[1], mousePoint)

    def getBoundingBox(self):
        hP1 = self.hotPoints[0]
        hP2 = self.hotPoints[1]

        x1, y1 = hP1.getX(), hP1.getY()
        x2, y2 = hP2.getX(), hP2.getY()

        if x1 < x2:
            x = x1
            width = x2 - x1
        else:
            x = x2
            width = x1 - x2
        if y1 < y2:
            y = y1
            height = y2 - y1
        else:
            y = y2
            height = y1 - y2

        return Rectangle(x, y, width, height)

    def duplicate(self):
        hP1 = self.hotPoints[0]
        hP2 = self.hotPoints[1]
        return LineSegment(Point(hP1.getX(), hP1.getY()), Point(hP2.getX(), hP2.getY()))

    def getShapeName(self):
        return 'Linija'
    
    def render(self, r):
        if self.isSelected():
            r.drawLine(self.hotPoints[0], self.hotPoints[1], 'red')
        else:
            r.drawLine(self.hotPoints[0], self.hotPoints[1], 'blue')