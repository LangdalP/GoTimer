import multiprocessing
from gui.buddy_gui import BuddyGui
from gui.bomb_timer_gui import TimerGui
from listener.gamestate_listener import ListenerWrapper


def main():
    # Message queue used for comms between processes
    queue = multiprocessing.Queue()
    gui = BuddyGui(queue)
    listener = ListenerWrapper(queue)

    gui.start()
    listener.start()

    gui.join()
    listener.shutdown()
    listener.join()

if __name__ == "__main__":
    main()
