import math
from pointrectangle import Point

class GeometryUtil:

    @staticmethod
    def distanceFromPoint(point1, point2):
        dX = point1.getX() - point2.getX()
        dY = point1.getY() - point2.getY()
        d = math.sqrt((dX)**2 + (dY)**2)
        return d

    @staticmethod
    def distanceFromLineSegment(s, e, p):
        
        sX, sY = s.getX(), s.getY()
        eX, eY = e.getX(), e.getY()
        pX, pY = p.getX(), p.getY()

        dX = eX - sX
        dY = eY - sY

        if dX == 0 and dY == 0:
            return GeometryUtil.distanceFromPoint(s, p)

        t = ((pX - sX) * dX + (pY - sY) * dY) / (dX**2 + dY**2)

        if t < 0:
            return GeometryUtil.distanceFromPoint(p, s)
        elif t > 1:
            return GeometryUtil.distanceFromPoint(p, e)
        else:
            x = sX + t * dX
            y = sY + t * dY
            return GeometryUtil.distanceFromPoint(p, Point(x, y))