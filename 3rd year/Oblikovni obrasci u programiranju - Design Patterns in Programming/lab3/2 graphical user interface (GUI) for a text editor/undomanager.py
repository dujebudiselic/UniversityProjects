class UndoManager:
    _instance = None

    def __init__(self):
        self.undoStack = []
        self.redoStack = []
        self.observers = []

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = UndoManager()
        return cls._instance

    def undo(self):
        action = self.undoStack.pop()
        action.execute_undo()
        self.redoStack.append(action)
        self.notifyObservers()

    def redo(self):
        action = self.redoStack.pop()
        action.execute_do()
        self.undoStack.append(action)
        self.notifyObservers()

    def push(self, c):
        self.redoStack.clear()
        self.undoStack.append(c)
        self.notifyObservers()

    def addObserver(self, o):
        self.observers.append(o)

    def removeObserver(self, o):
        if o in self.observers:
            self.observers.remove(o)

    def notifyObservers(self):
        if self.undoStack:
            canUndo = True
        else:
            canUndo = False
        if self.redoStack:
            canRedo = True
        else:
            canRedo = False
        for o in self.observers:
            o.updateUndo(canUndo, canRedo)