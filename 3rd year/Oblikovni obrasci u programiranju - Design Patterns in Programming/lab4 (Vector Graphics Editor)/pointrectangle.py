class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def translate(self, dp): 
        newX = self.x + dp.getX()
        newY = self.y + dp.getY()
        return Point(newX, newY)

    def difference(self, p):
        newX = self.x - p.getX()
        newY = self.y - p.getY()
        return Point(newX, newY)


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height