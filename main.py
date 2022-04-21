import json
import pymsgbox as pg

try:
    with open("installedApps.json", 'r') as f:
        pass
except FileNotFoundError:
    with open("installedApps.json", 'a') as f:
        dataSet = {
            "Reddit": "NO",
            "Instagram": "NO",
            "SnapChat": "NO",
            "Twitter": "NO",
            "Facebook": "NO",
            "Discord": "NO",
            "Telegram": "NO",
        }
        json.dump(dataSet, f, indent=4)
finally:
    with open("installedApps.json", 'r') as f:
        Apps = json.load(f)

def startTheBot():
    pg.confirm("BOT NAME", buttons=["Post", "App Management"])

startTheBot()