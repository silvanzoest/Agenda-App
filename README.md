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
  - "title": "String met titel van de afspraak"
  - "description": "String met een omschrijving van de afspraak"
  - "where": "String met de locatie"
  - "from": int die aangeeft wanneer de afspraak begint (zie Unix timestam en datetime.fromtimestamp)
  - "to": int die aangeeft wanneer de afspraak afgelopen is. Is -1 als er geen eindtijd ingevuld is.
  - "repeat": bool die aangeeft of deze afspraak herhaald moet worden.
  - "repeat_interval": int die aangeeft wanneer de afspraak opnieuw ingepland moet worden. (Nieuwe tijd is 'to + repeat_interval, of "from + repeat_interval" als "to == -1"). Gelijk aan -1 als 'repeat == False'
  - "repeat_times": int die aangeeft hoe vaak de afspraak herhaald moet worden. Gelijk aan -1 als 'repeat == False', 0 als de afspraak oneindig vaak herhaald moet worden.
  - "repeated": int die aangeeft hoe vaak de afspraak al herhaald is. Gelijk aan -1 als 'repeat == False' of 'repeat_times == 0'
  - "alert": boolean die aangeeft of een melding voor deze afspraak moet worden getoond
  - "alert_moments": list van integers die tijden aangeven wanneer alerts moeten worden getoond. Tijden worden berekend door 'from - int'
  - "attachments": list van strings die een path zijn naar een bijlage.
  - "in_trash": bool die aangeeft of deze afspraak momenteel in de prullenbak zit.
  - "moved_to_trash": int die aangeeft wanneer de afspraak naar de prullenbak is verplaatst. Is gelijk aan -1 als "in_trash == False"
  
### Instellingen
Alle instellingen zijn opgeslagen in een dictionary 'settings' in de communicatie/core.
De huidige instellingen zijn:
  - "language": Taal 
  - "appointment_decay_limit": Maximale tijd waarvoor een verlopen/afgelopen afspraak bewaard wordt.
  - "trash_timeout": Maximale tijd waarvoor een afpraak in de prullenbak bewaard wordt.
  
  
 ### Communicatie GUI en backend
 De GUI en de backend zijn gescheiden door een 'black box'. Deze black box heeft functies zodat de GUI en de 
 backend met elkaar kunnen communiceren. De API die ondersteund wordt is:
   - **core.api.dispatch(func_name: str, args, kwargs) -> typing.Any**:
      Call een geregistreerde functie met naam 'func_name'. args and kwargs zijn de argumenten voor deze functie.
   - **core.api.set_var(name: str, value: typing.Any) -> None**:
      Maak een global variable of verander de waarde van een global variable.
   - **core.api.get_var(name: str) -> typing.Any**:
      Vraag de waarde van een global variable op. De return waarde is een weakref.proxy naar het originele object.
   - **core.register(\*\*kwargs) -> None**:
      Registreer een functie voor gebruik voor de dispatch functie. De naam waaronder de functie geregistreerd wordt
      is de naam die gebruik is voor het keyword-argument.
   - **core.register(obj: types.FunctionType) -> types.FunctionType**: 
      Registreer een functie voor gebruik voor de dispatch functie. De naam waaronder de functie geregistreerd wordt 
      is de naam van de functie (obj.\__name\__)
   - **core.register(obj: type) -> type**:
      Registreer een class voor gebruik voor de dispatch functie. De naam waaronder de class geregistreerd wordt 
      is de naam van de class (obj.\__name\__)
   - **core.register_class(cls: type, register: int) -> None**: 
      register de verschillende onderdelen van een class. De delen van de class die geregistreerd moeten kunnen
      worden zijn:
        - De class zelf
        - class methods
        - static methods
        - class methods 
        - class  variables
      Welk delen precies geregistreerd worden kan worden bepaald met het register argument en bitflags.
   - **[global variable via get_var]: DATA_FILE**: pathlib.Path object met pad naar bestand met afspraken
   - **[global variable via get_var]: CONFIG_FILE**: pathlib.Path object met pad naar configuratiebestand 
   
 ### Opslaan en laden van bestanden
 Voor het laden en opslaan van de afspraken en instellingen is de volgende api beschikbaar:
  - **filesystem.load(path: pathlib.Path) -> dict[str: dict]**: Laad afspraken uit bestand 'path'. De functie moet ook controleren
   dat alle afspraken compatibel zijn met de huidige API door middel van de compat-API. Afspraken die niet compatibel zijn moeten
  met behulp van dezelfde API worden aangepast. Als alle afspraken zijn aangepast EN er tenminste EEN afspraak is aangpast,
  moeten alle afspraken eerste opnieuw opgeslagen worden.
  - **filesystem.save(path: pathlib.Path, data: dict[str: dict]) -> None**: Sla afspraken 'data' op in bestand 'path'.
  - **filesystem.load_config(path: pathlib.Path) -> dict[str: typing.Any]**: Laad instellingen uit bestand 'path'.
  - **filesystem.save_config(path: pathlib.Path, settings: dict[str: typing.Any) -> None**: Sla dictionary 'settings' op in bestand 'path'.
  - **[global variable via get_var]: file_format**: Global variable die aangeeft welk bestandsformaat moet worden gebruikt voor 
  het bestand met afspraken.
  - **[global variable via get_var]: config_file_format**: Global variable die aangeeft welk bestandsformaat moet worden
  gebruikt voor het configuratiebestand
  
  De bestandformaten die ondersteund moeten worden zijn:
  - json
  - xml
  - pickle 
  
  Voor het configuratie dient ook nog .properties ondersteund te worden.
  
### Algemene functies voor afspraken
De algemene functies voor het werken met afspraken zijn:
  - **appointments.get_appointments(sort_by=date, include_trash=False) -> typing.Iterator[str, dict]**: Iterator over alle afspraken 
  als (UUID, data) tuples. Als `include_trash` `True` is moeten ook items uit de prullenbak ge-yield te worden, anders niet. 
  Dit kan door de API van de prullenbak te gebruiken. De afspraken worden op gesorteerde volgorde ge-yield; sort_by geeft aan
  op welke manier. Zie voor meer informatie het kopje 'sorteren'
  - **appointments.add_appointment(data: Dict) -> str**: Voeg een afspraak toe aan de lijst met afspraken en genereer een UUID
  voor deze afspraak. Alle afspraken moeten opnieuw opgeslagen worden met behulp van de filesystem API.
  - **appointments.remove_appointment(uuid: str) -> typing.Union[str, None]**: Verwijder de afspraak met het gegeven UUID uit het 
  systeem; De lijst met afspraken dient opnieuw opgeslagen te worden. Als de afspraak opnieuw opgeslagen moet worden (zie kopje 'opslag
  afspraken') moet deze functie de relevante velden aanpassen, de afspraak opnieuw toevoegen en het nieuwe UUID returnen. 
  De return-waarde is anders `None`.
  - **appointments.update_appointments(uuid: str, data: dict) -> None**: Wijzig de gegeven afspraak door de corresponderende afspraak
  in de dict met afspraken te vervangen. De dictionary moet hierna opnieuw opgeslagen worden.
  - **appointments.get_old_appointments(sort_by=date, expiration_time: datetime.timedelta=one_week, include_trash=False) -> typing.Iterator[str, dict]**: Iterator over alle verlopen afspraken die minimaal `expiration_time` lang zijn verlopen, als 
  (UUID, data) tuples. Als `include_trash` `True` is moeten afspraken uit de prullenbak ook ge-yield worden. De afspraken worden op
  gesorteerde volgorde ge-yield; sort_by geeft aan op welke manier. Zie voor meer informatie het kopje 'sorteren'.
  - **appointments.clean_old_appointments(expiration_time: datetime.timedelta=one_week, include_trash=False) -> None**: Verwijder alle
  afspraken die al minimaal `expiration_time` lang zijn verlopen. Als `include_trash` `True` is moeten ook afspraken uit de 
  prullenbak worden verwijderd.
  
### Prullenbak
De prullenbak API bestaat uit de volgende functies:
  - **trash.get_trash_items(sort_by=date_moved_to_trash) -> Iterator[str, dict]**: Iterator over alle afspraken in de prullenbak als 
  als (UUID, data) tuples. `sort_by` geeft aan hoe de afspraken van te voren gesorteerd moeten worden. Zie voor meer informatie het kopje
  'sorteren'
  - **trash.clear_trash(expiration_time: datetime.timedelta=passed) -> None**: Verwijder alle afspraken die al `expiration_time` lang in 
  de prullenbak zitten. Als `expiration_time == -1` moeten alle afspraken die al geweest/verlopen zijn worden verwijderd.
  - **move_to_trash(uuid: str) -> None**: Verplaats een afspraak naar de prullenbak. Zet de globale variable `trash_history_id` gelijk
  aan het gegeven uuid. Zet de "in_trash" attribute van de afspraak naar True en zet de "moved_to_trash" attribute naar de huidige tijd.
  - **move_from_trash(uuid: str) -> None**: Haal een afspraak uit de prullenbak. Als de gegeven uuid gelijk is aan `trash_history_id`,
  moet deze globale variable naar `None` worden gezet. Zet de "in_trash" attribute van de afspraak naar False en zet de "moved_to_trash" attribute naar -1.
  - **[global variable via get_var]: trash_id: typing.Union[str, None]**: global variable met de uuid van de afspraak die
  als laatste naar de prullenbak is verplaatst.
  
### Compatibiliteit
De volgende functies helpen om afspraken van een oudere versie van de app te laten werken op een nieuwere versie:
  - **compat.validate_appointment(data: dict) -> bool**: return `True` als de gegeven dictionary in overeenstemming is met 
  de onder het kopje 'opslag afspraken' beschreven layout van een afspraak. return `False` als dit niet het geval is.
  - **compat.convert_appointment(data: dict) -> dict**: Pas de gegeven dictionary aan zodat deze in overeenstemming is 
  met de onder het kopje 'opslag afspraken' layout voor afspraken. Pas de gegeven dictionary **zelf** niet aan, maar maak een kopie.
  
### Utility
Dit is een module met een aantal willekeurige functies:
  - **util.save_appiontment(appointment: dict) -> None**: Sla een willekeurige afspraak op met de filesystem API
  - **util.save_config_var(name, value) -> None**: Sla de waarde van een instelling op met de filesystem API.
  
### Sorteren
De volgende vormen van sorteren moeten worden ondersteund:
  - by_date: Op volgorde van datum, oplopend
  - by_date_reversed: Op volgorde van datum, maar dan omgekeerd
  - [LET OP: hoeft _nog_ niet] importance; belangrijkheid
  - [Alleen voor de prullenbak]: date_moved_to_trash: Op volgorde van wanneer de afspraken naar de prullenbak zijn verplaatst.
  - [Alleen voor de prullenbak]: data_moved_to_trash_reversed: date_moved_to_trash maar dan omgekeerd.
  
