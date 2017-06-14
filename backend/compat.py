# Werk van Sil

# for-loop
# [] 


def validate_appointment(data: dict):
    KeyValDict = ['title': str, 'description': str,'where': str, 'from': int, "to": int, "repeat": bool, "repeat_interval": int}]
    for key in KeyValDict:
        if key not in dict:
            return False
        if type(data[key]) != KeyValDict[key]:
            return False
        else:
            continue
