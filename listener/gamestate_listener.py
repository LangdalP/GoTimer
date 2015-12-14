import json
import multiprocessing
import logging
from flask import Flask, request
from config import *
from messages import *
import requests

app = Flask(__name__)

message_queue = None


@app.route("/", methods=["POST"])
def main():
    process_data(request.data.decode("utf-8"))
    return ""


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return ''


def process_data(json_string):
    json_data = json.loads(json_string)
    added_key = json_data.get("added")
    if added_key:
        round_key = added_key.get("round")
        if round_key:
            bomb_key = round_key.get("bomb")
            win_team_key = round_key.get("win_team")
            if bomb_key:
                send_bomb_planted_message()
            elif win_team_key:
                send_round_over_message()


def send_bomb_planted_message():
    message_queue.put(BOMB_PLANTED)


def send_round_over_message():
    message_queue.put(ROUND_OVER)


def start_listener():
    if not DEBUG_ENABLED:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    app.run(port=3000, debug=DEBUG_ENABLED, use_reloader=False)


class ListenerWrapper(multiprocessing.Process):

    def __init__(self, msg_queue):
        multiprocessing.Process.__init__(self)
        self.msg_queue = msg_queue

    def run(self):
        global message_queue
        message_queue = self.msg_queue
        start_listener()

    def shutdown(self):
        requests.post("http://127.0.0.1:3000/shutdown", data={})
