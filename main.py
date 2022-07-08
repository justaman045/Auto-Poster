import os
from Provider.DataBase.DataBase import DataBase
from BotVersion import BotVersion as version
import sqlite3

try:
    import pymsgbox as pg
    import requests
except ModuleNotFoundError:
    os.system(f'pip install -r requirements.txt')
    os.system(f'python -m pip install --upgrade pip')
    print("\n\n\n\nPlease Restart this Software\n\n\n\nThanks for your Co-operation")
    exit()

def printMSG(message):
    space = int(len(message)+6)
    preStoredMessage = 'A new Update is available use `git pull` command to update'
    if space <= len(preStoredMessage):
        space += 76-space
    firstMessgaeSpace = int((space-len(preStoredMessage))/2)*" "
    SecondMessageSpace = int((space-len(message))/2)*" "
    print("*"*(space+2))
    print(f"*{space*' '}*")
    print(f"*{firstMessgaeSpace}{preStoredMessage}{firstMessgaeSpace}*")
    print(f"*{SecondMessageSpace}{message}{SecondMessageSpace}*")
    print(f"*{space*' '}*")
    print("*"*(space+2))

res = requests.get(
    "https://raw.githubusercontent.com/coderaman07/Auto-Poster/master/BotVersion.py")
LatestVersion = str(res.text).split(" = ")[1].replace("'", "").split(".")
CurrentVersion = str(version).split(".")
MajorUpdate,MinorUpdate,BugFixorPatches = False,False,False
if (LatestVersion[0] > CurrentVersion[0]):
    MajorUpdate = True
if (LatestVersion[1] > CurrentVersion[1]):
    MinorUpdate = True
if (LatestVersion[2] > CurrentVersion[2]):
    BugFixorPatches = True

if MajorUpdate == True:
    if MinorUpdate == True or BugFixorPatches == True:
        MinorUpdate, BugFixorPatches = False, False
    printMSG("It's a Major Update. Update it as soon as possible")
elif MinorUpdate == True:
    if BugFixorPatches == True:
        BugFixorPatches = False
    printMSG("It's a Minor Update. Update it as you will get new features")
elif BugFixorPatches == True:
    printMSG("It's a Bug Fix. Try Updating it as It may be related with your Privacy")

BotVersion = version

connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
DataBase.CheckOrCreateDefault()
import components.Post.Post
from components.App.AppManagement import getApps

config = cursor.execute('select * from "Bot Config"').fetchall()
connection.close()

def startTheBot():
    BotName = config[0][0]
    choice = pg.confirm(BotName, BotName,
               buttons=["Post", "App Management"])
    if choice == "Post":
        components.Post.Post.Post()
    elif choice == "App Management":
        try:
            getApps()
        finally:
            startTheBot()
    else:
        exit()

startTheBot()