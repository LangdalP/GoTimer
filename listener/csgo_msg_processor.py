from listener.msg_processor import *

class CsgoMsgProcessor(MsgProcessor):
    def __init__(self, model):
        self.model = model  # The processor will update the model according to messages

    def process(json_data):
        if "map" in json_data:
            process_map_data(json_data["map"])

    def process_map_data(map_data):
        if "name" in map_data:
            self.model.set_map(map_data["map"])
        if "phase" in map_data:
            self.model.set_game_status(map_data["phase"])
        if "round" in map_data: # Note: Usually round == team_ct + team_t, but there is some weird stuff on the first round
            pass
        if "team_ct" in map_data:
            pass
        if "team_t" in map_data:
            pass


