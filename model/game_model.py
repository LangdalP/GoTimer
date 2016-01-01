'''
Should contain:
Map
List of players
Game status - warmup, freezetime, live etc
Current round
Round-score
Who won each previous round
Scoreboard-data if possible

Things that might be better suited for other classes
Things specific to players (move scoreboard stuff to these)
'''

class GameModel:
    # Assumption: Model updates as the game goes along, nothing known initially
    def __init__(self):
        self.current_map = None
        self.player_list = []
        self.game_status = None
        self.round_status = None
        self.rounds = [None] * 30   # Contains who won each completed round
        self.obs_callbacks = []

    def set_map(self, map):
        if map == self.current_map:
            return
        self.current_map = map
        self.notify_observers()

    def set_players(self, players):
        self.player_list = players
        self.notify_observers()

    def set_game_status(self, status):
        if status == self.game_status:
            return
        self.game_status = status
        self.notify_observers()

    def set_round_status(self, status):
        self.round_status = status
        self.notify_observers()

    # Might have to change this based on the format of the data
    def set_rounds(self, rounds):
        self.rounds = rounds
        self.notify_observers()

    # Note: The rounds are zero-indexed in the model
    def set_round_score(self, round_no, round_winners):
        if round_no > (len(self.rounds) - 1):
            extra_rounds = [None] * 10
            self.rounds.extend(extra_rounds)
        if round_no > (len(self.rounds) - 1):
            raise Exception("Invalid round number!")
        self.rounds[round_no] = round_winners

    def get_num_completed_rounds(self):
        for i in range(len(self.rounds)):
            if self.rounds[i] is None:
                return i
        return len(self.rounds)

    def notify_observers(self, what=None):
        for obs in self.obs_callbacks:
            obs.model_changed(what)

