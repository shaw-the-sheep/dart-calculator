from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem

from models.Game import Game


class CreateGameInterface(Screen):
    double_triple_in = StringProperty("None")
    double_triple_out = StringProperty("None")

    initial_points = NumericProperty(301)

    def __init__(self, **kw):
        super().__init__(**kw)


    def back_home(self, instance):
        self.manager.current = "home"

    def set_in_option(self, value):
        self.double_triple_in = value

    def set_out_option(self, value):
        self.double_triple_out = value

    def on_initial_points_selected(self,     segmented_control: MDSegmentedControl,
    segmented_item: MDSegmentedControlItem):
        self.initial_points = int(segmented_item.text)
        print(self.initial_points)

    def start_game(self):
        nb_players = self.ids.number_of_players.nb
        nb_legs = self.ids.number_of_legs.nb
        nb_sets = self.ids.number_of_sets.nb
        game = Game.set_instance(
            initial_score= self.initial_points,
            nb_players= nb_players,
            nb_legs= nb_legs,
            nb_sets= nb_sets,
            options= {"in": self.double_triple_in, "out": self.double_triple_out}
        )

class CustomSpinBox(MDBoxLayout):
    nb = NumericProperty(1)
    difference = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def increase(self):
        self.nb += self.difference

    def decrease(self):
        if self.nb - 2 > 0:
            self.nb -= self.difference