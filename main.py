import json
import os
import pymsgbox as pg
from components.App.AppManagement import getApps
import components.Post.Post

try:
    with open("installedApps.json", 'r') as f:
        pass
except FileNotFoundError:
    with open("installedApps.json", 'a') as f:
        dataSet = {
            "Reddit": {
                "installed": "NO",
                "Detail": "Post on Reddit a Social Media Platform based on sub-reddits ( Communities ) without even opening Reddit"
            },
            "Twitter": {
                "installed": "NO",
                "Detail": "Post on Twitter a Social Media Platform will just tweet."
            },
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
               buttons=["Post", "App Management", "Contacts"])
    if choice == "Post":
        components.Post.Post.Post()
        # Run the Postin Method 
    elif choice == "App Management":
        try:
            getApps()
        finally:
            startTheBot()
        # Run the App Management
    else:
        exit()

startTheBot()