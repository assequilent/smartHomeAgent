# Конфиг (словарь порогов)
actions = {
    "maxHot": 26.0, # выше - включить охлаждение
    "minCold": 18.0, # ниже - включить отопление
    "maxDark": 50, # ниже - включить свет
    "maxLight": 200, # выше - выключить свет
}

# События датчиков
events = [
    {"room": "living_room", "temp": 21.5, "illuminance": 120, "motion": True,  "door": "closed", "mode": "auto"},
    {"room": "kitchen",     "temp": 22.0, "illuminance": 90,  "motion": True,  "door": "closed", "mode": "auto"},
    {"room": "hallway",     "temp": 20.5, "illuminance": 60,  "motion": False, "door": "open",   "mode": "alert"},
    {"room": "bedroom",     "temp": 27.5, "illuminance": 30,  "motion": False, "door": "closed", "mode": "night"},
    {"room": "living_room", "temp": 22.1, "illuminance": 250, "motion": True,  "door": "closed", "mode": "auto"},
    {"room": "kitchen",     "temp": 17.0, "illuminance": 100, "motion": False, "door": "closed", "mode": "auto"},
]


def tempRule(event):
    if event["temp"] > actions["maxHot"]:
        return "tempSETCOLD"
    if event["temp"] < actions["minCold"]:
        return "tempSETHOT"
    return "tempOK"


def lightRule(event):
    if event["illuminance"] < actions["maxDark"]:
        return "lightENABLE"
    if event["illuminance"] > actions["maxLight"]:
        return "lightDISABLE"
    return "lightOK"


def securityRule(event):
    if event["door"] == "open" and not event["motion"]:
        return "ALERT_doorOpened_!motion"
    if event["motion"] and event["mode"] == "alert":
        return "ALERT_motionInAlertMode"
    return "securityOK"


decisions = []
for event in events:
    decisions.append({
        "room": event["room"],
        "climate_action": tempRule(event),
        "security_action": securityRule(event),
        "light_action": lightRule(event),
    })

print("Решения агента умного дома:")
for d in decisions:
    print(d)