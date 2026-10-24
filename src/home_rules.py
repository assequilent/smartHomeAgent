# Конфиг (словарь порогов)
actions = {
    "maxHot": 26.0, # выше - включить охлаждение
    "minCold": 18.0, # ниже - включить отопление
    "maxDark": 50, # ниже - включить свет
    "maxLight": 200, # выше - выключить свет
}


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



def takeDecisions(events):
    decisions = []
    for event in events:
        decisions.append({
            "room": event["room"],
            "tempAction": tempRule(event),
            "securityAction": securityRule(event),
            "lightAction": lightRule(event),
        })
    return decisions
    
test_events = [
    {"room": "hall",    "temp": 22.0, "illuminance": 60,  "motion": False, "door": "open",   "mode": "alert"},
    {"room": "bedroom", "temp": 27.5, "illuminance": 30,  "motion": False, "door": "closed", "mode": "night"},
    {"room": "kitchen", "temp": 17.0, "illuminance": 250, "motion": True,  "door": "closed", "mode": "auto"},
]

assert tempRule(test_events[0]) == "tempOK"
assert tempRule(test_events[1]) == "tempSETCOLD"
assert tempRule(test_events[2]) == "tempSETHOT"

assert lightRule(test_events[1]) == "lightENABLE"
assert lightRule(test_events[2]) == "lightDISABLE"

assert securityRule(test_events[0]) == "ALERT_doorOpened_!motion"
assert securityRule(test_events[1]) == "securityOK"

print("Функции агента проверены")

result = takeDecisions(test_events)
for d in result:
    print(d)