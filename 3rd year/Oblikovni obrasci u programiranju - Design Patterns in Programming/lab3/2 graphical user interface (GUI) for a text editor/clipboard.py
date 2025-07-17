class ClipboardStack:
    def __init__(self):
        self.stack = []
        self.observers = []

    def addToClipboard(self, text):
        self.stack.append(text)
        self.notifyObservers()

    def removeFromClipboard(self):
        text = self.stack.pop()
        self.notifyObservers()
        return text

    def topOfClipboard(self):
        if self.stack:
            return self.stack[-1]
        else:
            return ''

    def isClipboardEmpty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False 

    def clearClipboard(self):
        self.stack.clear()
        self.notifyObservers()

    def addObserver(self, o):
        self.observers.append(o)

    def removeObserver(self, o):
        if o in self.observers:
            self.observers.remove(o)

    def notifyObservers(self):
        for o in self.observers:
            o.updateClipboard()