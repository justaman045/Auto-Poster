import json
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import pyperclip as clip
import pymsgbox as pg


def PostBox(title):
    root = Tk()
    root.geometry("500x500")
    root.title(title)
    root.resizable(width=False, height=False)
    PathOfImage = StringVar()
    Pos = StringVar()

    def GetImage():
        pathOfImage = askopenfilename(filetypes=[("Select Images", ".png .jpg .jpeg")])
        PathOfImage.set(pathOfImage)

    def MoveToNext():
        Post = textbox.get(1.0, "end-1c")
        Pos.set(Post)
        clip.copy(f"{Pos.get()}+{PathOfImage.get()}")
        root.destroy()

    labl = Label(root, text=f"{title} in the below TextBox")
    labl.config(font=("Courier", 12))
    labl.place(x=80, y=20)

    textbox = Text(root, height=15, width=60)
    textbox.place(x=8, y=60)

    btn = Button(root, text="Select Image", command=GetImage)
    btn.place(x=30, y=325)

    labl = Label(root, text=f"Particularly For Instagram and Snapchat")
    labl.config(font=("Courier", 11))
    labl.place(x=115, y=325)

    btn = Button(root, text="Next", command=MoveToNext)
    btn.place(x=100, y=400)

    root.mainloop()

def PlatformsToUpload():
    root = Tk()
    root.geometry("500x500")
    root.title("Select the Platforms to Upload")
    root.resizable(width=False, height=False)

    def MoveToNext():
        AllPlatformsSelected = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                AllPlatformsSelected += f"{key}+"
        clip.copy(AllPlatformsSelected)
        root.destroy()

    InstalledApps = []
    with open("installedApps.json", 'r') as f:
        Apps = json.load(f)
    with open("config.json", 'r') as f:
        config = json.load(f)

    for i in Apps:
        if str(Apps[i]) == "Yes":
            InstalledApps.append(i)
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            "None of the Apps are Installed.\n\nInstall Some Apps via App Management", config["BotName"])
        exit()
    else:
        for i in InstalledApps:
            optionCheckBox[f"{i}"] = IntVar()


    labl = Label(root, text=f"Select the Platforms to Upload")
    labl.config(font=("Courier", 12))
    labl.place(x=80, y=20)

    text = ScrolledText(root, width=60, height=15)
    text.place(x=8, y=60)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))

    btn = Button(root, text="Post", command=MoveToNext)
    btn.place(x=225, y=325)

    root.mainloop()


def PlatformsToUploadImages():
    root = Tk()
    root.geometry("500x500")
    root.title("Select the Platforms to Upload")
    root.resizable(width=False, height=False)

    def MoveToNext():
        AllPlatformsSelected = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                AllPlatformsSelected += f"{key}+"
        clip.copy(AllPlatformsSelected)
        root.destroy()

    InstalledApps = []
    with open("installedApps.json", 'r') as f:
        Apps = json.load(f)
    with open("config.json", 'r') as f:
        config = json.load(f)

    for i in Apps:
        if str(Apps[i]) == "Yes":
            InstalledApps.append(i)
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            "None of the Apps are Installed.\n\nInstall Some Apps via App Management", config["BotName"])
        exit()
    else:
        for i in InstalledApps:
            optionCheckBox[f"{i}"] = IntVar()

    labl = Label(root, text=f"Select the Platforms to Upload Images")
    labl.config(font=("Courier", 12))
    labl.place(x=80, y=20)

    text = ScrolledText(root, width=60, height=15)
    text.place(x=8, y=60)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))

    btn = Button(root, text="Post", command=MoveToNext)
    btn.place(x=225, y=325)

    root.mainloop()

# PlatformsToUpload()