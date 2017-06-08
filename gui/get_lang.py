"""
Dit is het bestand voor krijgen en terugsturen van de talen
Het heeft een aantal functies en dezen staat beschreven in de drive.

<LICENSE>
<COPYRIGHT NOTICE>
Animajosser <Animajosser@gmail.com>
"""

__version__="0.1"
__date__="08-06-2017"
__pythonversion__="3.5.2"

########################################################################################################################

# imports

import os

# variables
tussenquotes=False
languages={}

needed_list=[
    "topbar_file",
    "topbar_settings",
    "topbar_credits",
    "topbar_create_appointment",
    "topbar_trash",
    "topbar_close",
    "credits_text",
    "credits_popup_title",
]

# functions

def get_lang_from_file():
    """ This returns the language, read from the settings file """
    pass

def assign(line):
    further = False
    first = False
    name = ""
    key = ""
    for a in line:
        if a=="|":
            name=name[:-1]
            further=True
            first=True
        elif not further:
            name+=a
        elif further and first:
            first=False
        elif a=="\n":
            continue
        else:
            key+=a
    return name, key

# script

language="en"

file=open(os.path.join("lang", language+".lang"), mode="r")

for a in file:
    if "#" not in a and a!="" and a!=" ":
        if '"""' in a:
            if not tussenquotes:
                tussenquotes=True
            else:
                tussenquotes=False
        if not tussenquotes and not '"""' in a:
            name, key=assign(a)
            languages[name]=key
        else:
            if tussenquotes and '"""' in a:
                name, key=assign(a.replace('"""', ""))
                key+="\n"
            elif tussenquotes:
                key+=a
            else:
                key+=a.replace('"""', "")
                languages[name]=key


for a in needed_list:
    if a not in languages:
        print(a, "was'nt found in the file:", language+".lang")
        languages[a]="N/A"
