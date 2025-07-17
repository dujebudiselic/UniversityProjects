class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def getRow(self):
        return self.row
    
    def getColumn(self):
        return self.column

class LocationRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def reverseIfNeeded(self):
        if (self.start.getRow(), self.start.getColumn()) <= (self.end.getRow(), self.end.getColumn()):
            return self.start, self.end
        return self.end, self.start

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end