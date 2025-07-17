from abc import ABC, abstractmethod

class Renderer(ABC):

    @abstractmethod
    def drawLine(self, s, e, color):
        pass

    @abstractmethod
    def fillPolygon(self, points, color):
        pass

class G2DpyRenderer(Renderer):
    def __init__(self, canvas):
        self.canvas = canvas

    def drawLine(self, s, e, color):
        self.canvas.create_line(s.getX(), s.getY(), e.getX(), e.getY(), fill=color)

    def fillPolygon(self, points, color):
        x_y = []
        for p in points:
            x_y.append(p.getX())
            x_y.append(p.getY())
        self.canvas.create_polygon(*x_y, fill='blue', outline=color)