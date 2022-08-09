import os

try:
    import sqlite3
    import sys
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    from tkinter.scrolledtext import ScrolledText
    import pyperclip as clip
    import pymsgbox as pg
except ModuleNotFoundError:
    os.system('pip install -r requirements.txt')
    os.system('python -m pip install --upgrade pip')
    print("\n\n\n\nPlease Restart this Software\n\n\n\nThanks for your Co-operation")
    exit()


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

    def keyPressed(e):
        Post = textbox.get(1.0, "end-1c")
        if len(Post) <= 280:
            stringData = f"You've got {280 - len(Post)} Charecters left"
            labl3.config(text=stringData)
            try:
                btn3.config(state='normal')
            except:
                pass
        else:
            btn3.config(state='disabled')
            stringData = f"You've exceeded {len(Post) - 280} Charecters. Please Remove {len(Post) - 280} Charecters"
            labl3.config(text=stringData)

    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    Apps = cursor.execute('select * from Apps').fetchall()
    connection.close()
    InstalledApps = []

    for i in Apps:
        if str(i[1]) == "Yes":
            InstalledApps.append(i[0])
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            "None of the Apps are Installed.\n\nInstall Some Apps via App Management", config[0])
        sys.exit()
    else:
        for i in InstalledApps:
            optionCheckBox[f"{i}"] = IntVar()

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

    labl3 = Label(root, text=f"You've got 280 Charecters left")
    labl3.config(font=("Courier", 11))
    labl3.place(x=90, y=375)
    textbox.bind('<KeyPress>', keyPressed)

    btn3 = Button(root, text="Next", command=MoveToNext)
    btn3.place(x=225, y=430)

    root.mainloop()

def PlatformsToUpload(Image):
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
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    Apps = cursor.execute('select * from Apps').fetchall()
    connection.close()

    for i in Apps:
        if str(i[1]) == "Yes":
            if len(Image) == 0 and i[0] not in ['Instagram']:
                InstalledApps.append(i[0])
            elif len(Image) != 0:
                InstalledApps.append(i[0])
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            "None of the Apps are Installed.\n\nInstall Some Apps via App Management", config[0])
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
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    Apps = cursor.execute('select * from Apps').fetchall()
    connection.close()

    for i in Apps:
        if str(i[1]) == "Yes":
            InstalledApps.append(i[0])
    optionCheckBox = {}

    if len(InstalledApps) == 0:
        pg.alert(
            "None of the Apps are Installed.\n\nInstall Some Apps via App Management", config[0])
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


def MultiPurposeOptionBox(title, options, ErrorMsg):
    root = Tk()
    root.geometry("500x500")
    root.title(title)
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


# MultiPurposeOptionBox("Hello", [
#                       "Hey", 'world', "how", 'are', 'you'], "")
