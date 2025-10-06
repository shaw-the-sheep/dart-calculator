from models.Player import Player
from models.utils import check_options, calculate_total_score


def singleton(cls):
    class SingletonClass(cls):
        _instance = None
        _init_args = None
        _init_kwargs = None

        @classmethod
        def set_instance(cls, *args, **kwargs):
            if cls._instance is None:
                cls._init_kwargs = kwargs
                cls._init_args = args
                cls._instance = cls(*args, **kwargs)
            return cls._instance

        @classmethod
        def get_instance(cls):
            if cls._instance is not None:
                return cls._instance
            return ""

        @classmethod
        def reset_instance(cls):
            cls._instance = None

            if cls._init_args is not None and cls._init_kwargs is not None:
                cls._instance = cls(*cls._init_args, **cls._init_kwargs)

        @classmethod
        def delete_instance(cls):
            cls._instance = None

        cls.set_instance = staticmethod(set_instance)
        cls.get_instance = staticmethod(get_instance)
        cls.reset_instance = staticmethod(reset_instance)
        cls.delete_instance = staticmethod(delete_instance)

    return  SingletonClass


@singleton
class Game:
    def __init__(self, initial_score, nb_players, nb_legs, nb_sets, options: dict):
        self.initial_score = initial_score
        self.nb_players = nb_players
        self.players = self.generate_players(nb_players)
        self.players[0].playing = True
        self.nb_legs = nb_legs
        self.nb_sets = nb_sets
        self.in_option = options["in"]
        self.out_option = options["out"]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.throws = []
        self.game_end = False
        self.have_a_winner = False

    def generate_players(self, nb_players):
        list_of_players = []
        for i in range(1, nb_players+1):
            name = "Player " + str(i)
            status = True if i == 1 else False
            list_of_players.append(
                Player(name=name, score=self.initial_score, status=status)
            )
        return list_of_players

    def players_data(self):
        list_data = []
        for player in self.players:
            p = {"player_name": player.name, "player_score": player.score, "is_playing": player.playing}
            list_data.append(p)
        return list_data

    def next(self):
        print("next is called")
        self.current_player.playing = False
        if self.current_player_index == len(self.players) -1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.current_player = self.players[self.current_player_index]
        self.current_player.playing = True

    def win_the_game(self, shots:list):
        total = calculate_total_score(shots)
        if self.current_player.score - total == 0:
            return True
        return False

    def player_throw(self, shot):
        if len(self.throws) >=3:
            return
        print(self.throws)
        if not self.current_player.in_option_checked and len(self.throws) == 0:
            if not check_options(self.in_option, shot):
                print("you need a " + self.in_option)
                self.next()
                return
            self.current_player.in_option_checked = True
        print("option checked")
        if self.current_player.is_busted([shot]):
            self.add_score()
            self.next()
            return

        if self.win_the_game([shot]) and check_options(self.out_option, shot):
            self.current_player.history.append(shot)
            print(self.current_player.name + " won the game")
            self.game_end = True
            return

        self.throws.append(shot)
        self.current_player.validate_shots([shot])

    def next_turn(self):
        if self.game_end:
            return
        if len(self.throws) == 3:
            self.next()
            self.throws.clear()
            return True
        return False

    def previous(self):
        self.throws.clear()
        if self.current_player_index == 0:
            self.current_player_index = len(self.players) -1
        else:
            self.current_player_index -= 1
        self.current_player = self.players[self.current_player_index]
        self.add_score()

    def add_score(self):
        shots = []
        if len(self.throws) > 0:
            shots = self.throws
        else:
            shots = self.current_player.history[-3:]
            self.current_player.history = self.current_player.history[:-3]

        score = calculate_total_score(shots)
        self.current_player.score += score

    def clear_current_throws_from_history(self):
        items_to_delete = self.current_player.history[-len(self.throws):]
        score = calculate_total_score(items_to_delete)
        self.current_player.score += score
        self.current_player.history = self.current_player.history[:-len(self.throws)]

    def delete_last_throw(self):
        t = self.throws.pop()
        self.current_player.history.pop()
        score = calculate_total_score([t])
        self.current_player.score += score

    def end_of_leg(self):
        self.current_player.legs_won += 1
        if self.current_player.legs_won == self.nb_legs:
            self.current_player.sets_won += 1
            if self.current_player.sets_won == self.nb_sets:
                self.have_a_winner = True
        self.reinitialization()


    def reinitialization(self, all_the_game=False):
        if not self.have_a_winner:
            self.reinitialize_player_data()
            self.current_player_index = self.current_player_index + 1 if self.current_player_index < len(self.players)-1 else 0
            self.players[self.current_player_index].playing = True
            self.current_player = self.players[self.current_player_index]
            self.throws = []
            self.game_end = False
        # when the whole game needs to be reinitialized.

    def reinitialize_player_data(self):
        for p in self.players:
            p.score = self.initial_score
            p.history = []
