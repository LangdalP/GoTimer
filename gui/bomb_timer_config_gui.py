from tkinter import *


class ConfigDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        Label(self.top, text="Test").pack()

        self.e = Entry(self.top)
        self.e.pack(padx=5)

        b = Button(self.top, text="Ok", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        print(self.e.get())
        self.top.destroy()

