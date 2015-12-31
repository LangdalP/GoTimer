from tkinter import *
import configparser as parser


class ConfigDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.title("Configuration")

        Label(self, text="GoBuddy Configuration").grid(row=0, column=0, padx=5, pady=2)
        self.e = Entry(self)
        self.e.grid(row=1, padx=5, pady=2)

        Entry(self).grid(row=2, padx=5, pady=2)

        Button(self, text="Save", command=self.ok).grid(row=3, padx=5, pady=2)

        self.init()

    def init(self):
        config = parser.ConfigParser()
        config.read("config.ini")

        text_value = config["TestSection"]["TextEntry"]
        self.e.insert(0, text_value)

    def ok(self):
        print(self.e.get())
        with open("config.ini", "w") as cfg_file:
            config = parser.ConfigParser()
            config.add_section("TestSection")
            config.set("TestSection", "TextEntry", self.e.get())
            config.write(cfg_file)
        self.destroy()

