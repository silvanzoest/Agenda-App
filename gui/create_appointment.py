"""
Dit is het bestand voor het afspraak-maak-scherm van de Agenda-App
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
print("Importing Builder")
from kivy.lang.builder import Builder

# Layouts
print("Importing BoxLayout")
from kivy.uix.boxlayout import BoxLayout

print("Load kv File Create appointment Screen")
Builder.load_file('create_appointment.kv')

# Classes #


# Main widgets

class AppointmentCreationScreen(BoxLayout):
    pass
# screens


class AppointmentCreationWindow(App):
    """Appointment screen"""

    icon = 'icon.ico'
    title = '<Create Appointment>'

    def build(self):

        return AppointmentCreationScreen()

# Script

if __name__=='__main__':
    AppointmentCreationWindow().run()