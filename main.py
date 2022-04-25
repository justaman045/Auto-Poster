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
            "Instagram": {
                "installed": "NO",
                "Detail": "Post on Instagram a Social Media Platform with a Image and captions ( Post )"
            },
            "SnapChat": {
                "installed": "NO",
                "Detail": "Post on Snapchat a Social Media Platform this will basically upload a new Snap"
            },
            "Twitter": {
                "installed": "NO",
                "Detail": "Post on Twitter a Social Media Platform will just tweet."
            },
            "Facebook": {
                "installed": "NO",
                "Detail": "Post on Facebook a Social Media Platform will Post a Text on a desired Page with Image ( Optional )"
            },
            "Discord": {
                "installed": "NO",
                "Detail": "Post on Discord a Social Media Platform for Gamers"
            },
            "Telegram": {
                "installed": "NO",
                "Detail": "Post on Telegram a Social Media Platform on a particular Channel"
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
               buttons=["Post", "App Management"])
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