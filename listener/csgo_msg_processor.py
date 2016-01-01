from listener.msg_processor import *

class CsgoMsgProcessor(MsgProcessor):
    def __init__(self, model):
        self.model = model  # The processor will update the model according to messages

    def process(self, json_data):
        if "map" in json_data and "round" in json_data:
            process_map_and_round_data(json_data["map"], json_data["round"])

    def process_map_and_round_data(self, map_data, round_data):
        if "name" in map_data:
            self.model.set_map(map_data["map"])
        if "phase" in map_data:
            self.model.set_game_status(map_data["phase"])
        if "win_team" in round_data:
            winning_team = round_data["win_team"]
            round_no = map_data["round"] - 1
            self.model.set_round_score(round_no, winning_team)
