
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

# noinspection PyUnresolvedReferences
from controllers.create_game_controller import CreateGameInterface
# noinspection PyUnresolvedReferences
from controllers.option_controller import OptionsInterface
# noinspection PyUnresolvedReferences
from controllers.game_controller import GameInterface

from models.Game import Game

Builder.load_file("options.kv")
Builder.load_file("home.kv")
Builder.load_file("create_game.kv")
Builder.load_file("game.kv")

game = None

class AppBar(MDBoxLayout):
    title = StringProperty("Home")
    icon_name = StringProperty("information")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        Game.delete_instance()

class HomeNavigation(Button):
    pass


class HomeInterface(Screen):
    def options(self, instance):
        self.manager.current = "options"

    def create_game(self, instance):
        self.manager.current = "create"

class LoadGameInterface(Screen):
    pass

class ScreenM(ScreenManager):
    pass

class MyWindow(MDBoxLayout):
    pass

class DartCalculatorApp(MDApp):
    def build(self):
        return Builder.load_file("gui.kv")

    def on_stop(self):
        Game.delete_instance()

if __name__ == "__main__":
    DartCalculatorApp().run()

