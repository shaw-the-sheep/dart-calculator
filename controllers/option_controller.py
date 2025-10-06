from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen


class OptionsInterface(Screen):
    language = StringProperty("english")
    with_voice_commande = BooleanProperty(True)
    dark_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def voice_is_checked(self, instance, value):
        self.with_voice_commande = value
        print(self.with_voice_commande)

    def dark_mode_is_checked(self, instance, value):
        self.dark_mode = value
        print(self.dark_mode)

    def select_language(self, value):
        self.language = value
        print(self.language)