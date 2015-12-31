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
        self.rounds = []    # Contains who won each completed round
        self.obs_callbacks = []

    def set_map(self, map):
        self.current_map = map
        self.notify_observers()

    def set_players(self, players):
        self.player_list = players
        self.notify_observers()

    def set_game_status(self, status):
        self.game_status = status
        self.notify_observers()

    def set_round_status(self, status):
        self.round_status = status
        self.notify_observers()

    # Might have to change this based on the format of the data
    def set_rounds(self, rounds):
        self.rounds = rounds
        self.notify_observers()

    def notify_observers(self, what=None):
        for obs in self.obs_callbacks:
            obs.model_changed(what)

