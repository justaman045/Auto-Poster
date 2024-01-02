
import os
# from components.Module_Installer.main import InstallAllModules

try:
    import sqlite3
    from tkinter.filedialog import askopenfilename
    import pymsgbox as pg
    from tkinter import *
    import instagrapi as insta
except ModuleNotFoundError:
    # InstallAllModules()
    pass

# # driverpth = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# photopath = askopenfilename(filetypes=[("Select Images", ".png .jpg .jpeg")])
# phototext = "Testing the Image"


def UploadTOIG(Image, videos, description, username):
    if len(username) != 1:
        for i in username:
            UploadToInstagram(Image, videos, description, i)
    else:
        UploadToInstagram(Image, videos, description, username[0])

def UploadToInstagram(Image, videos, description, username):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    userdetails = cursor.execute(f'select * from Instagram where username="{username}"').fetchall()
    username = userdetails[0][0]
    passwd = userdetails[0][1]
    client = insta.Client()
    client.login(username=username, password=passwd)
    client.dump_settings("./Provider/Instagram/dump.json")
    client.get_timeline_feed()
    if Image != None and Image != "":
        client.photo_upload(caption=description, path=Image)
    if videos != None and videos != "":
        client.clip_upload(path=videos, caption=description)
    exit()
    
    

def InstallInstagram():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    username = pg.prompt('Enter your Instagram Username', config[0])
    if username == None:
        exit()
    password = pg.prompt('Enter your Instagram Password', config[0])
    if password == None:
        exit()
    browserPath = askopenfilename()
    if len(username) != 0 and len(password) != 0:
        cursor.execute('create table if not exists Instagram ( username Text, password Text, browserPath Text )')
        connection.commit()
        cursor.execute(f'insert into Instagram values ( "{username}", "{password}", "{browserPath}" )')
        cursor.execute(
            'update Apps set isInstalled = "Yes" where Platform = "Instagram"')
        connection.commit()
        return "Done"
    else:
        pg.alert('Creadentials not entered Properly\n\nNone of the things were saved.', config[0])
    connection.close()
    return ' Error'


def GuideInstagram():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    pg.alert('Enter your Username and Password when Prompted and then select your browser to open Instagram', config[0])
    connection.close()


def UpdateAndDeleteInstagram():
    TableName = "Instagram"
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    Apps = cursor.execute(f'select * from {TableName}').fetchall()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    tempPlace = 1
    tempPlacee = 0


    def InstagramUpdate(username):
        user = cursor.execute(
            f'select * from "{TableName}" where username="{username}"').fetchall()[0]
        newUsername = pg.prompt(
            f"Enter the New User ( If Changed )\n\nCurrent Username is {user[0]}", config[0], default=user[0])
        if newUsername == None:
            exit()
        newPassword = pg.prompt(
            f"Enter the New Password ( If Changed )\n\nCurrent Username is {user[1]}", config[0], default=user[1])
        if newPassword == None:
            exit()
        pg.alert("In the Next step we'll ask your browser Location Select the old one if you do not want to change the Browser")
        data = str(user[2]).split("/")[-1]
        data = str(user[2]).replace(f"/{data}", "")
        newBrowserLocation = askopenfilename(initialdir=data)
        if newUsername == user[0] and newPassword == user[1] and newBrowserLocation == user[2]:
            pg.alert("Nothing has been changed so nothing is changed in DataBase")
        else:
            cursor.execute(
                f'update "{TableName}" set "username"="{newUsername}", "password"="{newPassword}", "browserPath"="{newBrowserLocation}" where "username"="{user[0]}"')
            connection.commit()


    def InstagramDelete(username):
        cursor.execute(f'delete from "{TableName}" where username="{username}"')
        connection.commit()


    root = Tk()
    root.geometry("700x500")
    root.title("App Configuration")
    root.resizable(height=False, width=False)

    textLabel = Label(root, text=f"{TableName} Configuration")
    textLabel.config(font=(20))
    textLabel.place(x=250, y=20)

    canvas = Canvas(root, width=600, height=400)
    frame = Frame(canvas)
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)

    for AppData in Apps:
        AppLabel = Label(frame, text=AppData[0], height=5)
        AppLabel.grid(padx=(30, 0))
        Button(frame, width=10, command=lambda m=AppData[0]: InstagramUpdate(m),
            text="Update").grid(row=tempPlacee, column=1, padx=(90, 0))
        Button(frame, width=10, command=lambda m=AppData[0]: InstagramDelete(m),
            text="Delete").grid(row=tempPlacee, column=1, padx=(250, 0))

        tempPlacee += 1

    canvas.create_window(0, 0, anchor='nw', window=frame, width=600)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                    yscrollcommand=scroll_y.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    canvas.focus_set()
    canvas.place(x=50, y=50)

    root.mainloop()


# UploadToInstagram(askopenfilename(filetypes=[("Select Images", ".png .jpg .jpeg .mov .mp4 .mkv .ts")]), "Test Desc", "1stay_consistent")