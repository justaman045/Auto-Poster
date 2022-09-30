import sqlite3
from BotVersion import BotVersion as version
from components.Module_Installer.main import InstallAllModules
try:
    import requests
except ModuleNotFoundError:
    InstallAllModules()


def Update():
    def printMSG(message):
        preStoredMessage = 'A new Update is available use `git pull` command to update'
        toUpdateInstruction = " If You've cloned or downoaded directly from `github.com/coderaman7/Auto-Poster` just use `git pull` "
        toUpdateInstructiontwo = "or if you've forked it Pull the latest commits on your repo then run `git pull` "
        def getSpace(getMessageSpace):
            return " "*int((len(toUpdateInstruction)+3 - len(getMessageSpace))/2)
        print("*"*(len(toUpdateInstruction)+5))
        print(f"*{(len(toUpdateInstruction)+3)*' '}*")
        print(f"*{getSpace(preStoredMessage)}{preStoredMessage}{getSpace(preStoredMessage)}*")
        print(f"*{getSpace(message)}{message}{getSpace(message)}*")
        print(f"*{(len(toUpdateInstruction)+3)*' '}*")
        print(f"*{getSpace(toUpdateInstruction)}{toUpdateInstruction}{getSpace(toUpdateInstruction)} *")
        print(f"*{getSpace(toUpdateInstructiontwo)}{toUpdateInstructiontwo}{getSpace(toUpdateInstructiontwo)}*")
        print(f"*{(len(toUpdateInstruction)+3)*' '}*")
        print("*"*(len(toUpdateInstruction)+5))

    res = requests.get(
        "https://raw.githubusercontent.com/coderaman07/Auto-Poster/master/BotVersion.py")
    LatestVersion = str(res.text).split(" = ")[1].replace("'", "").split(".")
    CurrentVersion = str(version).split(".")
    MajorUpdate, MinorUpdate, BugFixorPatches = False, False, False
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

def checkUpdateAndUpdate():
    Update()
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    data = cursor.execute("select * from 'Bot Config'").fetchall()
    if int(str(data[0][1]).split(".")[0]) != int(str(version).split(".")[0]):
        updateCommand = cursor.execute(f"update 'Bot Config' set Version='{version}'")
        connection.commit()
    elif int(str(data[0][1]).split(".")[1]) != int(str(version).split(".")[1]):
        updateCommand = cursor.execute(
            f"update 'Bot Config' set Version='{version}'")
        connection.commit()
    elif int(str(data[0][1]).split(".")[2]) != int(str(version).split(".")[2]):
        updateCommand = cursor.execute(
            f"update 'Bot Config' set Version='{version}'")
        connection.commit()
    connection.close()
