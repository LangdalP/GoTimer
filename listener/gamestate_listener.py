import json
import multiprocessing
import http.server
import socketserver
import urllib.request
from config import *
from messages import *


class PostHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args):
        http.server.SimpleHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        print(self.path)
        if self.path == "/shutdown":
            self.server.should_be_running = False
        else:
            length = int(self.headers["Content-Length"])
            post_body = self.rfile.read(length).decode("utf-8")
            self.process_post_data(post_body)
        self.send_ok_response()

    def process_post_data(self, json_string):
        json_data = json.loads(json_string)
        added_key = json_data.get("added")
        if added_key:
            round_key = added_key.get("round")
            if round_key:
                bomb_key = round_key.get("bomb")
                win_team_key = round_key.get("win_team")
                if bomb_key:
                    self.send_bomb_planted_message()
                elif win_team_key:
                    self.send_round_over_message()

    def send_bomb_planted_message(self):
        self.server.msg_queue.put(BOMB_PLANTED)

    def send_round_over_message(self):
        self.server.msg_queue.put(ROUND_OVER)

    def send_ok_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


class ListenerServer(socketserver.TCPServer):

    def __init__(self, server_address, req_handler_class, msg_queue):
        self.msg_queue = msg_queue
        self.should_be_running = True
        socketserver.TCPServer.__init__(
            self, server_address, req_handler_class)

    def serve_forever(self):
        while self.should_be_running:
            self.handle_request()


class ListenerWrapper(multiprocessing.Process):

    def __init__(self, msg_queue):
        multiprocessing.Process.__init__(self)
        self.msg_queue = msg_queue
        self.server = None

    def run(self):
        self.server = ListenerServer(
            ("127.0.0.1", 3000), PostHandler, self.msg_queue)
        self.server.serve_forever()

    def shutdown(self):
        req = urllib.request.Request("http://127.0.0.1:3000/shutdown", data=b"")
        urllib.request.urlopen(req)
