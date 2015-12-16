import multiprocessing
from gui.bomb_timer_gui import TimerGui
from listener.gamestate_listener import ListenerWrapper

if __name__ == "__main__":
    # Message queue used for comms between processes
    queue = multiprocessing.Queue()
    gui = TimerGui(queue)
    listener = ListenerWrapper(queue)

    gui.start()
    listener.start()

    gui.join()
    listener.shutdown()
    listener.join()
