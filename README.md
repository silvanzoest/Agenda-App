# Agenda-App
De eerste app van onze programmeerclub: een simpele app om afspraken bij te houden.

## Inhoud:
  - Gebruik Github
  - Documentatie backend
  
## Gebruik Github
### Bestand uploaden
Navigeer naar het bestand waar jij aan werkt. Klik daarna op het potloodje. In het venster dat dan geopend wordt kun je verandering in het bestand op Github aanbrengen; Het makkelijkst is om de inhoud van het bestand op je computer te plakken in het venster. Onder aan de pagina vul je bij titel "[naam bestand] - Jouw naam" in. Beschrijf in het veld daaronder kort wat je veranderd/toegevoegd hebt.

### Bestand downloaden
Navigeer naar het goede bestand en klik op "raw". Kopieer de tekst en plak het in een bestand op je computer.


## Documentatie backend
### Inhoud:
  - Opslag afspraken
  - Instellingen
  - Communicatie GUI en backend
  - Opslaan en laden van bestanden
  - Algemene functies voor afpraken
  - Prullenbak
  - Compatabiliteit
  - Utility functies
  - Sorteren
  
### Opslag afspraken
Alle afspraken zijn opgeslagen in een global variable in de communiatie/core, onder de naam 'appointments'.
Dit is een dictionary waarin de keys de UUID (unieke identifier) van een afspraak is.
De value die bij de key hoort is een dictionary met de data van de afspraak. 
Op het moment heeft deze dictionary de volgende velden:
  - title: "String met titel van de afspraak"
  - "description": "String met een omschrijving van de afspraak"
  - "where": "locatie"
  - "from": int die aangeeft wanneer de afspraak begint (zie Unix timestam en datetime.fromtimestamp)
  - "to": int die aangeeft wanneer de afspraak afgelopen is. Is -1 als er geen eindtijd ingevuld is.
  - "repeat": bool die aangeeft of deze afspraak herhaald moet worden.
  - "repeat_interval": int die aangeeft wanneer de afspraak opnieuw ingepland moet worden. (Nieuwe tijd is 'to + repeat_interval, of "from + repeat_interval" als "to == -1"). Gelijk aan -1 als 'repeat == False'
  - "repeat_times": int die aangeeft hoe vaak de afspraak herhaald moet worden. Gelijk aan -1 als 'repeat == False', 0 als de afspraak oneindig vaak herhaald moet worden.
  - "repeated": int die aangeeft hoe vaak de afspraak al herhaald is. Gelijk aan -1 als 'repeat == False' of 'repeat_times == 0'
  - "alert": boolean die aangeeft of een melding voor deze afspraak moet worden getoond
  - "alert_moments": list van integers die tijden aangeven wanneer alerts moeten worden getoond. Tijden worden berekend door 'from - int'
  - "attachments": list van strings die een path zijn naar een bijlage.
  
### Instellingen
Alle instellingen zijn opgeslagen in een dictionary 'settings' in de communicatie/core.
De huidige instellingen zijn:
  - "language": Taal 
  - "appointment_decay_limit": Maximale tijd waarvoor een verlopen/afgelopen afspraak bewaard wordt.
  - "trash_timeout": Maximale tijd waarvoor een afpraak in de prullenbak bewaard wordt.
  
  
 ### Communicatie GUI en backend
 De GUI en de backend zijn gescheiden door een 'black box'. Deze black box heeft functies zodat de GUI en de 
 backend met elkaar kunnen communiceren. De API die ondersteund wordt is:
   - core.api.dispatch(func_name: str, args, kwargs) -> typing.Any
      Call een geregistreerde functie met naam 'func_name'. args and kwargs zijn de argumenten voor deze functie.
   - core.api.set_var(name: str, value: typing.Any) -> None
      Maak een global variable of verander de waarde van een global variable.
   - core.api.get_var(name: str) -> typing.Any
      Vraag de waarde van een global variable op. De return waarde is een weakref.proxy naar het originele object.
   - core.register(\*\*kwargs) -> None
      Registreer een functie voor gebruik voor de dispatch functie. De naam waaronder de functie geregistreerd wordt
      is de naam die gebruik is voor het keyword-argument.
   - core.register(obj: types.FunctionType) -> types.FunctionType
      Registreer een functie voor gebruik voor de dispatch functie. De naam waaronder de functie geregistreerd wordt 
      is de naam van de functie (obj.__name__)
   - core.register(obj: type) -> type
      Registreer een class voor gebruik voor de dispatch functie. De naam waaronder de class geregistreerd wordt 
      is de naam van de class (obj.__name__)
   - core.register_class(cls: type, register: int) -> None
      register de verschillende onderdelen van een class. De delen van de class die geregistreerd moeten kunnen
      worden zijn:
        - De class zelf
        - class methods
        - static methods
        - class methods 
        - class  variables
      Welk delen precies geregistreerd worden kan worden bepaald met het register argument en bitflags.
   - [global variable via get_var]: DATA_FILE: pathlib.Path object met pad naar bestand met afspraken
   - [global variable via get_var]: CONFIG_FILE: pathlib.Path object met pad naar configuratiebestand 
