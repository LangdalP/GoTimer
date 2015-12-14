import multiprocessing
from bomb_timer_gui import TimerGui
from gamestate_listener import ListenerWrapper

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    gui = TimerGui(queue)
    listener = ListenerWrapper(queue)

    gui.start()
    listener.start()

    gui.join()
    listener.shutdown()
    listener.join()
