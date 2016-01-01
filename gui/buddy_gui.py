from tkinter import *
import time
import os
import math
import multiprocessing
from queue import Empty
from misc.config import *
from misc.messages import *
from model.game_model import GameModel
from listener.csgo_msg_processor import CsgoMsgProcessor

BUDDY_FONT = ("Helvetica", 14)


class BuddyCanvas(Canvas):

    def __init__(self, parent, width, height, model=None):
        Canvas.__init__(self, parent, width=width, height=height,
                        bd=0, highlightthickness=0, relief='ridge')
        self.parent = parent
        self.model = model
        self.canv_width = width
        self.canv_height = height
        self.set_text("Placeholder")
        self.model.obs_callbacks.append(self)   # Add self as observer

    def update_canvas(self):
        canvas_string = ""
        if self.model is not None:
            if self.model.current_map is not None:
                canvas_string = canvas_string + self.model.current_map + "\n"
            if self.model.game_status is not None:
                canvas_string = canvas_string + self.model.game_status + "\n"

        self.set_text(canvas_string)

    def model_changed(self, what):
        print("Got a \"model changed\" callback in the canvas")
        self.update_canvas()

    def set_text(self, text, colour=FG_COLOUR):
        self.delete("all")
        text_pos = (self.canv_width / 2, self.canv_height / 2)
        self.create_text(
            text_pos, text=text, font=BUDDY_FONT, fill=colour)



class BuddyGui(multiprocessing.Process):

    def __init__(self, msg_queue):
        multiprocessing.Process.__init__(self)
        self.queue = msg_queue
        self.model = None
        self.msg_proc = None
        self.root = None
        self.gui = None

    def check_messages(self):
        try:
            msg = self.queue.get_nowait()
            self.msg_proc.process(msg)
        except Empty:
            pass

        self.root.after(GUI_CHECK_MSG_INTERVAL, self.check_messages)

    def run(self):
        self.root = Tk()
        self.root.configure(background=BG_COLOUR)
        self.root.title("GoBuddy")

        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        if "nt" == os.name:
            self.root.wm_iconbitmap(bitmap = os.path.join(parent_dir, "gt_icon.ico"))

        self.model = GameModel()
        self.msg_proc = CsgoMsgProcessor(self.model)

        self.gui = BuddyCanvas(self.root, TIMER_WIDTH, TIMER_HEIGHT, self.model)
        self.gui.configure(background=BG_COLOUR)
        self.gui.pack()

        self.check_messages()
        self.root.mainloop()
