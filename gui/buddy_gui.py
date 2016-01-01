from tkinter import *
import time
import os
import math
import multiprocessing
from queue import Empty
from misc.config import *
from misc.messages import *
from gui.bomb_timer_config_gui import *
from model.game_model import GameModel


class BuddyCanvas(Canvas):

    def __init__(self, parent, width, height):
        Canvas.__init__(self, parent, width=width, height=height,
                        bd=0, highlightthickness=0, relief='ridge')
        self.parent = parent
        self.create_text(
            TEXT_POSITION, text=IDLE_TEXT, font=FONT, fill=FG_COLOUR)

    def set_text(self, text, colour=FG_COLOUR):
        self.delete("all")
        self.create_text(
            TEXT_POSITION, text=text, font=FONT, fill=colour)



class BuddyGui(multiprocessing.Process):

    def __init__(self, msg_queue):
        multiprocessing.Process.__init__(self)
        self.queue = msg_queue
        self.root = None
        self.gui = None

    def check_messages(self):
        try:
            msg = self.queue.get_nowait()
            if msg == BOMB_PLANTED:
                self.gui.start_timer()
            elif msg == ROUND_OVER:
                self.gui.stop_timer = True
            else:
                pass
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
        self.msg_processor = CsgoMsgProcessor(model)

        self.gui = BuddyCanvas(self.root, TIMER_WIDTH, TIMER_HEIGHT)
        self.gui.configure(background=BG_COLOUR)
        self.gui.pack()

        self.check_messages()
        self.root.mainloop()
