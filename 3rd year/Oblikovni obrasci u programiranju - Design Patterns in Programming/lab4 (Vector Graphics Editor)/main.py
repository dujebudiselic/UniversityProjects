from GUI import GUI
from linesegment import LineSegment
from oval import Oval

def main():
    objects = []
    objects.append(LineSegment())
    objects.append(Oval())
    master = GUI(objects)
    master.mainloop()

if __name__ == '__main__':
    main()