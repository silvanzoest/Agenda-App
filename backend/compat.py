def validate_appointment(data: dict):
    KeyValDict = {'title': str, 'description': str, 'where': str, 'from': int, "to": int, "repeat": bool, "repeat_interval": int, "repeat_times": int, "repeated": int, "alert": bool, "alert_moments": list, "attachements": list, "in_trash": bool, "moved_to_trash", int}
        for key in KeyValDict:
            if key not in dict:
                return False
            if type(data[key]) != KeyValDict[key]:
                return False
            else:
                continue



    if data["repeat"] == False and (data["repeat_interval"] != -1 or data["repeat_times"]):
       return  False
    if 
