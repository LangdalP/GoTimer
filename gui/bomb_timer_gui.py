from tkinter import *
import time
import os
import math
import multiprocessing
from queue import Empty
from misc.config import *
from misc.messages import *


class TimerCanvas(Canvas):

    def __init__(self, parent, width, height):
        Canvas.__init__(self, parent, width=width, height=height,
                        bd=0, highlightthickness=0, relief='ridge')
        self.parent = parent
        self.create_text(
            TEXT_POSITION, text=IDLE_TEXT, font=FONT, fill=FG_COLOUR)
        self.start_time = None
        self.stop_timer = False
        self.timer_running = False

    def start_timer(self, start_time=BOMB_TIME):
        if self.timer_running:
            return
        self.stop_timer = False
        self.start_time = time.clock()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        now = time.clock()
        time_left = BOMB_TIME - (now - self.start_time)

        if self.stop_timer:
            self.set_text(IDLE_TEXT)
            self.timer_running = False
        elif time_left < 0:
            self.set_text(IDLE_TEXT)
            self.timer_running = False
        else:
            self.set_time_left(time_left)
            self.after(11, self.update_timer)

    def set_text(self, text, colour=FG_COLOUR):
        self.delete("all")
        self.create_text(
            TEXT_POSITION, text=text, font=FONT, fill=colour)

    def set_time_left(self, seconds):
        time_left_text = create_time_string_from_seconds(seconds)
        if seconds < WITH_DEFUSER_THRESHOLD:
            self.set_text(time_left_text, WITH_DEFUSER_COLOUR)
        elif seconds < WITHOUT_DEFUSER_THRESHOLD:
            self.set_text(time_left_text, WITHOUT_DEFUSER_COLOUR)
        elif seconds < HURRY_UP_THRESHOLD:
            self.set_text(time_left_text, HURRY_UP_COLOUR)
        else:
            self.set_text(time_left_text)


# Probably not idiomatic python
def create_time_string_from_seconds(time_left_seconds):
    seconds = math.floor(time_left_seconds)
    centis = (time_left_seconds % 1) * 100
    centis_string = "%02.0f" % centis
    # Corner case when time is exactly x:00
    if centis_string == "100":
        centis_string = "99"
    return "{secs}:{centis}".format(secs=seconds, centis=centis_string)


class TimerGui(multiprocessing.Process):

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
        self.root.title("GoTimer")

        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        if "nt" == os.name:
            self.root.wm_iconbitmap(bitmap = os.path.join(parent_dir, "gt_icon.ico"))

        self.gui = TimerCanvas(self.root, TIMER_WIDTH, TIMER_HEIGHT)
        self.gui.configure(background=BG_COLOUR)
        self.gui.pack()

        self.check_messages()
        self.root.mainloop()
