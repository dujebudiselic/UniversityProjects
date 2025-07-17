from listeners import DocumentModelListener
from renderer import G2DpyRenderer
from pointrectangle import Point
import tkinter as tk

class DrawingCanvas(tk.Canvas, DocumentModelListener):
    def __init__(self, master, documentModel):
        super().__init__(master, bg='white', width=600, height=600)
        self.documentModel = documentModel
        self.renderer = G2DpyRenderer(self)
        self.documentModel.addDocumentModelListener(self)
        self.bind('<ButtonPress-1>', self.onMouseDown)
        self.bind('<ButtonRelease-1>', self.onMouseUp)
        self.bind('<B1-Motion>', self.onMouseDragged)
        self.bind('<Key>', self.onKeyPressed)
        self.focus_set() 

        self.redraw()

    def redraw(self):
        self.delete("all")
        for o in self.documentModel.list():
            o.render(self.renderer)
            self.master.currentState.afterDraw(self.renderer, o)
        self.master.currentState.afterDraw_(self.renderer)

    def documentChange(self):
        self.redraw()

    def onMouseDown(self, event):
        mousePoint = Point(event.x, event.y)
        shift = bool(event.state & 0x0001)
        ctrl = bool(event.state & 0x0004)
        self.master.currentState.mouseDown(mousePoint, shift, ctrl)

    def onMouseUp(self, event):
        mousePoint = Point(event.x, event.y)
        shift = bool(event.state & 0x0001)
        ctrl = bool(event.state & 0x0004)
        self.master.currentState.mouseUp(mousePoint, shift, ctrl)

    def onMouseDragged(self, event):
        mousePoint = Point(event.x, event.y)
        self.master.currentState.mouseDragged(mousePoint)

    def onKeyPressed(self, event):
        self.master.currentState.keyPressed(event)