from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout

from models.Game import Game
from models.utils import get_former_index


class GameInterface(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nb_legs = 1
        self.nb_sets = 1

    def backspace_hit(self):
        Game.get_instance().delete_last_throw()
        self.ids.players_view.update_info()

    def next_player(self):
        if Game.get_instance().game_end:
            self.end_of_leg()
            return
        if Game.get_instance().next_turn():
            self.ids.players_view.switch_player(next_=True)

    def on_enter(self):
        self.ids.players_view.populate()
        self.nb_legs = Game.get_instance().nb_legs
        self.nb_sets = Game.get_instance().nb_sets

    def end_of_leg(self):
        Game.get_instance().end_of_leg()
        self.ids.players_view.reinitialize_info()
        if Game.get_instance().have_a_winner:
            self.winner()

    def winner(self):
        winner_name = Game.get_instance().current_player.name
        content = PopUpContent(text=f"{winner_name} is the winner", screen_manager= self.manager,
                               player_view= self.ids.players_view)
        win = Popup(title="Winner !", content=content, size_hint=(0.6, 0.7), background_color = (250, 250, 250))
        win.open()

class PopUpContent(MDBoxLayout):
    winner = StringProperty("")

    def __init__(self, text, screen_manager, player_view, **kwargs):
        super(PopUpContent, self).__init__(**kwargs)
        self.winner = text
        self.screen_manager = screen_manager
        self.player_view = player_view

    def restart_game(self):
        print("game restarting")
        self.parent.parent.parent.dismiss()
        Game.reset_instance()
        self.player_view.clear_widgets()
        self.player_view.populate()

    def restart_game_with_different_parameters(self):
        print("restart with diffrent parameters")
        self.parent.parent.parent.dismiss()
        Game.delete_instance()
        self.screen_manager.current = "create"

    def go_home(self):
        print("go home")
        self.parent.parent.parent.dismiss()
        Game.delete_instance()
        self.screen_manager.current = "home"

class NumberZone(MDGridLayout):
    shot = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 5
        self.rows = 5
        self.spacing = 0

        for i in range(1, 21):
            self.number_btn(i)

        self.number_btn("25")
        self.number_btn("50")
        self.number_btn("T")
        self.number_btn("D")
        self.number_btn("AC")

    def enter_your_throw(self, instance):
        number = instance.text
        players_view = self.parent.parent.ids.players_view
        game = Game.get_instance()
        if number == "T" or number == "D":
            self.shot += number
        elif number == "AC":
            game.clear_current_throws_from_history()
            players_view.update_info()
            game.previous()
            players_view.switch_player(next_=False)
            players_view.update_info()
        else:
            if 4 > len(self.shot) > 0 :
                try:
                    if "T" in self.shot and int(number) > 20:
                        self.shot = ""
                    elif "D" and int(number) > 20:
                        self.shot = ""
                except ValueError:
                    return
            self.shot += number
            game.player_throw(self.shot)
            players_view.update_info()
            self.shot = ""


    def number_btn(self, value):
        b = Button(text=str(value), size_hint=(0.2, 0.2), background_color = (26/255, 209/255, 255/255, 1))
        b.bind(on_press=self.enter_your_throw)
        self.add_widget(b)

class Player(MDBoxLayout):
    player_name = StringProperty("")
    player_score = NumericProperty(0)
    is_playing = BooleanProperty(False)
    history_list = StringProperty("")
    nb_legs = NumericProperty(0)
    nb_sets = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_turn(self):
        self.is_playing = True

    def end_turn(self):
        self.is_playing = False

    def update_view(self, player = None):
        if player is None:
            player = Game.get_instance().current_player
        self.history_list =  ", ".join(reversed(player.history))
        self.player_score = player.score
        self.update_sets_legs(player)

    def update_sets_legs(self, player):
        print(f"{player.name}: sets: {player.sets_won} legs: {player.legs_won}")
        self.nb_sets = player.sets_won
        self.nb_legs = player.legs_won

class PlayersView(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.bind(width=self.update_cols)
        self.size_hint_y = None
        self.widgets = []

    def update_cols(self, *args):
        self.cols = self.width // 300

    def populate(self):
        self.clear_widgets()
        players = Game.get_instance().players

        for player in players:
            p = Player(
                player_name = player.name,
                player_score = player.score,
                is_playing = player.playing
            )

            self.add_widget(p)
            self.widgets.append(p)

    def update_info(self):
        index = Game.get_instance().current_player_index
        self.widgets[index].update_view()

    def reinitialize_info(self):
        for index in range(len(self.widgets)):
            player = Game.get_instance().players[index]
            self.widgets[index].update_view(player)

    def switch_player(self, next_):
        index = Game.get_instance().current_player_index
        self.widgets[index].start_turn()
        prev_index = get_former_index(next_, index)
        self.widgets[prev_index].end_turn()