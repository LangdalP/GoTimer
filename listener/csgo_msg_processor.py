from listener.msg_processor import *

class CsgoMsgProcessor(MsgProcessor):
    def __init__(self, model):
        self.model = model  # The processor will update the model according to messages

    def process(json_data):
        if "map" in json_data:
            process_map_data(json_data["map"])

    def process_map_data(map_data):
        if "name" in map_data:
            pass
        if "phase" in map_data:
            pass
        if "round" in map_data:
            pass
        if "team_ct" in map_data:
            pass
        if "team_t" in map_data:
            pass


