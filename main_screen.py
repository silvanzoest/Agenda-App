"""
Dit is het bestand voor het algemene scherm van de Agenda-App
Het heeft een aantal functies en dezen staat beschreven in de drive.

<LICENSE>
<COPYRIGHT NOTICE>
Animajosser <Animajosser@gmail.com>
"""
__version__="0.0"
__date__="09-04-2017"
__Kivyversion__="1.10.0"
##############################################################################################

# imports #

# Most important
print("Importing App")
from kivy.app import App
print("Importing config and disabling multitouch")
from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
print("Importing Window")
from kivy.core.window import Window
print("Importing Builder")
from kivy.lang.builder import Builder

# Layouts
print("Importing BoxLayout")
from kivy.uix.boxlayout import BoxLayout
print("Importing StackLayout")
from kivy.uix.stacklayout import StackLayout

# Attributes
print("Importing Button")
from kivy.uix.button import Button
print("Importing TextInput")
from kivy.uix.textinput import TextInput
print("Importing CheckBox")
from kivy.uix.checkbox import CheckBox
print("Importing Label")
from kivy.uix.label import Label

# popups
print("Importing Popup")
from kivy.uix.popup import Popup

print("load kv File")
Builder.load_file('main_screen.kv')

# Classes #

class BaseScreen(BoxLayout):
    pass

class AgendaApp(App):
    """Home class"""

    icon = 'icon.ico'
    title = '<Agenda App>'

    def build(self):

        Window.clearcolor=(1, 1, 1, 1)

        return BaseScreen()

# Script

if __name__=='__main__':
    AgendaApp().run()