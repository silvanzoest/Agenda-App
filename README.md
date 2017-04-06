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
