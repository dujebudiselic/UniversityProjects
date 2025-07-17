import tkinter as tk

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=500, height=500, bg='white')
        self.pack(fill=tk.BOTH, expand=True)

        self.create_line(15, 25, 200, 25, fill='red', width=1)
        self.create_line(25, 15, 25, 200, fill='red', width=1)

        self.create_text(150, 120, text='Duje')
        self.create_text(150, 140, text='Buda', fill='blue')

        self.focus_set()

        self.bind('<Return>', self.closeWindow)

    def closeWindow(self, event):
        self.master.destroy()


master = tk.Tk()
master.title('Zasebni prozor')
component = Canvas(master)
master.mainloop()

