"""
Dit is het bestand voor het algemene scherm van de Agenda-App
Het heeft een aantal functies en dezen staat beschreven in de drive.

<LICENSE>
<COPYRIGHT NOTICE>
Animajosser <Animajosser@gmail.com>
"""
__version__="0.1"
__date__="08-06-2017"
__kivyversion__="1.10.0"
__pythonversion__="3.5.2"
##############################################################################################

# imports #

# Most important
print("Importing App")
from kivy.app import App
print("Importing config and disabling multitouch")
from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
#print("Importing Window")
#from kivy.core.window import Window
print("Importing Builder")
from kivy.lang.builder import Builder

# Layouts
print("Importing BoxLayout")
from kivy.uix.boxlayout import BoxLayout
#print("Importing StackLayout")
#from kivy.uix.stacklayout import StackLayout

# Attributes
#print("Importing Button")
#from kivy.uix.button import Button
#print("Importing TextInput")
#from kivy.uix.textinput import TextInput
#print("Importing CheckBox")
#from kivy.uix.checkbox import CheckBox
print("Importing Label")
from kivy.uix.label import Label

# popups
print("Importing Popup")
from kivy.uix.popup import Popup

# kv's
print("Load kv File Home Screen")
Builder.load_file('main_screen.kv')

# python modules

print("Importing Time")
import time
print("Importing subprocess")
import subprocess

# Classes #

# Main widgets

class CreditsPopup(Popup):
    pass

class BaseScreen(BoxLayout):
    creditspopup=CreditsPopup()

# Screens

class AgendaApp(App):
    """Home class and home screen"""

    icon = 'icon.ico'
    title = 'Agenda App'

    def build(self):

        return BaseScreen()

    def open_app_crea_scr(self):
        global AppointmentCreationScreen
        # not tested yet
        AppointmentCreationScreen = subprocess.Popen('python3 create_appointment.py', shell=True)

    def close_app_crea_scr(self):
        global AppointmentCreationScreen
        AppointmentCreationScreen.kill()

    # Easter Egg

    t0 = False
    easter_egg = Popup(
        size_hint=(.75, .75), auto_dismiss=True,
        title="Pieter rookt peukjes",
        content=Label(text="Roken is heel ongezond\n Doo Da Doo Da"))
    # This is quite buggy, but I just had to make an easter egg
    def start_measure_time(self):
        self.t0 = time.time()
    def stop_measure_time(self):
        if self.t0:
            t1 = time.time()
            time_used=t1-self.t0
            if time_used>=5:
                self.easter_egg.open()
                self.t0=False


# Script

if __name__=='__main__':
    AgendaApp().run()