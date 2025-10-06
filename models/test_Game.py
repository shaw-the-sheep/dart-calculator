from unittest import TestCase

from models.Game import Game


class TestGame(TestCase):
    def test_player_throw(self):
        Game.delete_instance()
        self.game = Game.set_instance(
            initial_score= 301,
            nb_players= 2,
            nb_legs= 1,
            nb_sets= 1,
            options= {"in": "None", "out": "None"}
        )
        self.game.player_throw("T20")
        self.game.player_throw("T20")
        self.game.player_throw("T20")
        self.game.next_turn()
        self.game.player_throw("T20")
        self.game.player_throw("T20")
        self.game.player_throw("T20")
        self.game.next_turn()
        self.game.player_throw("T20")
        self.game.player_throw("T20")
        self.game.player_throw("1")
        self.game.next_turn()
        self.assertEquals(self.game.current_player.name, "Player 1")
