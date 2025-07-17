import tkinter as tk
from documentmodel import DocumentModel
from state import IdleState, AddShapeState, SelectShapeState
from drawingcanvas import DrawingCanvas

class GUI(tk.Tk):
    def __init__(self, objects):
        super().__init__()
        self.objects = objects
        self.title('Drawing')

        self.documentModel = DocumentModel()
        self.currentState = IdleState()

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        for o in objects:
            button = tk.Button(toolbar, text=o.getShapeName(), command=lambda obj=o: self.setAddShapeState(obj))
            button.pack(side=tk.LEFT, padx=2, pady=2)

        button = tk.Button(toolbar, text='Select', command=lambda: self.setSelectShapeState())
        button.pack(side=tk.LEFT, padx=2, pady=2)
        self.canvas = DrawingCanvas(self, self.documentModel)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bind('<Key>', self.onKeyPress)

    def setAddShapeState(self, obj):
        self.currentState.onLeaving()
        self.currentState = AddShapeState(self.documentModel, obj)

    def setSelectShapeState(self):
        self.currentState.onLeaving()
        self.currentState = SelectShapeState(self.documentModel)

    def onKeyPress(self, event):
        if event.keysym == 'Escape':
            self.currentState.onLeaving()
            self.currentState = IdleState()
        else:
            self.currentState.keyPressed(event.keycode)