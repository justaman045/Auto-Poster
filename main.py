import json
import os
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
try:
    with open("config.json", 'r') as f:
        pass
except FileNotFoundError:
    BotName = pg.prompt("Enter the Bot Name", "Enter the Bot Name", f"{os.getlogin()}'s Bot")
    with open("config.json", 'a') as f:
        dataSet = {
            "BotName": BotName,
            "version": 2.0
        }
        json.dump(dataSet, f, indent=4)
finally:
    with open("config.json", 'r') as f:
        config = json.load(f)

def startTheBot():
    choice = pg.confirm(config["BotName"], config["BotName"],
               buttons=["Post", "App Management"])
    if choice == "Post":
        print("Post")
        # Run the Postin Method 
    elif choice == "App Management":
        print("App Management")
        # Run the App Management
    else:
        exit()

startTheBot()