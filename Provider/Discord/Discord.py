import json
import os
import sqlite3
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import requests, pymsgbox as pg
from tkinter import *
import pyperclip as clip

# from components.GraphicalElements.PostBox import MultiPurposeOptionBox


def sendMSG(message, authorization, channelID, image):
    payload = {
        'content': message
    }
    if image != "":
        files = {
            'file': (image, open(image, 'rb')),

        }
    header = {
        "authorization": authorization
    }
    if image != "":
        r = requests.post(
            f"https://discord.com/api/v9/channels/{channelID}/messages", headers=header, data=payload, files=files)
    else:
        r = requests.post(
            f"https://discord.com/api/v9/channels/{channelID}/messages", headers=header, data=payload)

def createDiscordConfig():

    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    try:
        cursor.execute('drop table Discord')
        connection.commit()
    except:
        authorizationKey = pg.prompt("Enter the Authorization KEY : \n\nFor Guide on how to obtain the Auhorization key Select Install with guide in App Management", config[0])
        UserName = pg.prompt(
            "Enter your Discord Username", config[0])
        if authorizationKey == None and UserName != None:
            exit()
        else:
            channelID = pg.prompt("Enter Channel ID of where you want to Send the Message.", config[0])
            channelName = pg.prompt("Enter Channel Name from which you'll be addressing thing ( In this Bot ONLY )", config[0])
            if channelID != None and channelName != None:
                cursor.execute('create table Discord ( username VarChar2, authorizationKey VarChar2, ChannelID VarChar2, ChannelName VarChar2 )')
                cursor.execute(f'insert into Discord values ( "{UserName}", "{authorizationKey}", "{channelID}", "{channelName}" )')
                cursor.execute('update Apps set isInstalled = "Yes" where Platform = "Discord"')
                connection.commit()
    connection.close()
    return 'Done'


def MultiPurposeOptionBox(title, options, ErrorMsg):
    root = Tk()
    root.geometry("500x500")
    root.title(title)
    root.resizable(width=False, height=False)
    print(options)

    def MoveToNext():
        AllPlatformsSelected = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                AllPlatformsSelected += f"{key}+"
        clip.copy(AllPlatformsSelected)
        root.destroy()

    InstalledApps = []
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    connection.close()

    for i in options:
        InstalledApps.append(i)
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            ErrorMsg, config["BotName"])
        exit()
    else:
        for i in InstalledApps:
            optionCheckBox[f"{i}"] = IntVar()

    text = ScrolledText(root, width=60, height=15)
    text.place(x=8, y=60)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))

    btn = Button(root, text="Post", command=MoveToNext)
    btn.place(x=225, y=325)

    root.mainloop()


def sendDiscordMessage(Post, Image, discordConfig, channels):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    discord = cursor.execute('select * from Discord').fetchall()
    for i in discord:
        discordConfig.append(i[3])
    authorizationKeys = []
    for i in channels:
        authorizationKeys = cursor.execute(
            f'select * from Discord where ChannelName = "{i}"').fetchall()
    channel = [x[3] for x in authorizationKeys]
    for chan in authorizationKeys:
        for channe in channels:
            if channe == chan[3]:
                sendMSG(Post, chan[1], chan[2], Image)
    
def deleteDiscordConfig():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    try:
        cursor.execute('drop table Discord')
        connection.commit()
    except:
        pass
    return 'Done'

def GuidedInstallDiscord():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    connection.close()
    pg.alert("Open Discord and in Settings under Advanced Settings Turn on Developer Mode",
             config[0])
    pg.alert("Then Copy the Channel Id by right clicking on it and click select Copy ID",
             config[0])
    pg.alert("Remember : To Add the user to send msg through this bot open discord in browser and select the last Integer like string\n\nExample : https://discord.com/channels/@me/826522141704060949 is the user's link the copy 826522141704060949 and this is our ID for that user",
             config[0])


def AddChannel():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    username = pg.prompt("Enter your UserName on Discord", config[0])
    data = cursor.execute(f'select * from Discord where username = "{username}"').fetchone()
    try:
        if len(data) == 4:
            channelID = pg.prompt(
                "Enter Channel ID of where you want to Send the Message.", config[0])
            channelName = pg.prompt(
                "Enter Channel Name from which you'll be addressing thing ( In this Bot ONLY )", config[0])
            if channelID != None and channelName != None:
                cursor.execute(
                    f'insert into Discord values ( "{username}", "{authorizationKey}", "{channelID}", "{channelName}" )')
    except:
        authorizationKey = pg.prompt(
            "Enter the Authorization KEY : \n\nFor Guide on how to obtain the Auhorization key Select Install with guide in App Management", config[0])
        if authorizationKey == None and username != None:
            exit()
        else:
            channelID = pg.prompt(
                "Enter Channel ID of where you want to Send the Message.", config[0])
            channelName = pg.prompt(
                "Enter Channel Name from which you'll be addressing thing ( In this Bot ONLY )", config[0])
            if channelID != None and channelName != None:
                cursor.execute(
                    f'insert into Discord values ( "{username}", "{authorizationKey}", "{channelID}", "{channelName}" )')
    connection.commit()    
    connection.close()

# AddChannel()
