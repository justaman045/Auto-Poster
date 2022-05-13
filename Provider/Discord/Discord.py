import json
import os
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import requests, pymsgbox as pg
from tkinter import *
import pyperclip as clip

from components.GraphicalElements.PostBox import MultiPurposeOptionBox


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
    try:
        with open("config.json", 'r') as f:
            botconfig = json.load(f)
        currentPath = os.getcwd()
        pathDir = os.path.join("Provider", "Discord")
        os.chdir(pathDir)
        with open("discord.json", 'r') as f:
            config = json.load(f)
    except:
        
        authorizationKey = pg.prompt(
            "Enter the Authorization KEY : \n\nFor Guide on how to obtain the Auhorization key Select Install with guide in App Management", botconfig['BotName'])
        if authorizationKey == None:
            exit()
        else:
            channelID = pg.prompt(
                "Enter Channel ID of where you want to Send the Message.", botconfig['BotName'])
            channelName = pg.prompt(
                "Enter Channel Name from which you'll be addressing thing ( In this Bot ONLY )", botconfig['BotName'])
            if channelID != None and channelName != None:
                with open("discord.json", 'w') as f:
                    dataSet = {
                        channelName: channelID
                    }
                    json.dump(dataSet, f, indent=4)
                with open("authorization.dtc", 'w') as f:
                    dataSet = {
                        'authKey': authorizationKey
                    }
                    json.dump(dataSet, f, indent=4)
    os.chdir(currentPath)
    return 'Done'


def sendDiscordMessage(Post):
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Discord")
    os.chdir(pathDir)
    with open('discord.json', 'r') as f:
        discordConfig = json.load(f)
    os.chdir(currentPath)

    options = [x for x in discordConfig.keys()]

    MultiPurposeOptionBox("Select on which Channels you want to send Message", options, "Discord App has been currupted in you local machine ( Please Re-install the app again from App Management )")
    channels = str(clip.paste()).split("+")
    channels = channels[:-1]
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Discord")
    os.chdir(pathDir)
    with open('authorization.dtc', 'r') as f:
        auth = json.load(f)
    for i in discordConfig:
        if i in channels:
            sendMSG(Post, auth['authKey'], discordConfig[i])
    os.chdir(currentPath)
    
def deleteDiscordConfig():
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Discord")
    os.chdir(pathDir)
    with open('discord.json', 'w') as f:
        f.write("")
    with open('authorization.dtc', 'w') as f:
        f.write("")
    os.chdir(currentPath)
    return 'Done'

def GuidedInstallDiscord():
    with open("config.json", 'r') as f:
        botconfig = json.load(f)
    pg.alert("Open Discord and in Settings under Advanced Settings Turn on Developer Mode",
             botconfig['BotName'])
    pg.alert("Then Copy the Channel Id by right clicking on it and click select Copy ID",
             botconfig['BotName'])
    pg.alert("Remember : To Add the user to send msg through this bot open discord in browser and select the last Integer like string\n\nExample : https://discord.com/channels/@me/826522141704060949 is the user's link the copy 826522141704060949 and this is our ID for that user",
             botconfig['BotName'])


image = askopenfilename(
    filetypes=[("Select Images", ".png .jpg .jpeg")])
sendMSG("Hello", "OTc0NTk2MTA4MDgyODc2NDI2.GSOHFa.NSjS437OxesuODYHD7F2J7AVtN7EPXJOimH_SU",
        "974597594728767519", image)
