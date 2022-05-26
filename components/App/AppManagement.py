import sqlite3
from tkinter import *
import pymsgbox as pg
from Provider.Discord.Discord import AddChannel, GuidedInstallDiscord, createDiscordConfig, deleteDiscordConfig
from Provider.Instagram.Instagram import GuideInstagram, InstallInstagram

from Provider.Reddit.Reddit import CreateRedditConfig, DeleteRedditConfig, RedditGuideToInstall
from Provider.Twitter.Twitter import APISetup, AddHashtag, InstallTwitter, UnInstallTwitter

def getApps():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    Apps = cursor.execute('select * from Apps').fetchall()
    connection.close()
    tempPlace = 1
    tempPlacee = 0

    def CreateAppConfig(App, guided):
        if App == 'Reddit':
            if guided == True:
                RedditGuideToInstall()
            return CreateRedditConfig()
        if App == 'Twitter':
            if guided == True:
                APISetup()
            return InstallTwitter()
        if App == 'Discord':
            if guided == True:
                GuidedInstallDiscord()
            return createDiscordConfig()
        if App == 'Instagram':
            if guided == True:
                GuideInstagram()
            return InstallInstagram()

    def DeleteAppConfig(App):
        if App == 'Reddit':
            return DeleteRedditConfig()
        if App == 'Twitter':
            return UnInstallTwitter()
        if App == 'Discord':
            return deleteDiscordConfig()
        if App == 'Instagram':
            return deleteDiscordConfig()

    def CreateConfig(AppName, guided = False):
        for App in Apps:
            if App[0] == AppName:
                if App[1] == 'No':
                    CreateAppConfig(AppName, guided)
                elif App[1] == 'Yes':
                    choice = pg.confirm(f"This will Uninstall {AppName} and Clear all the Application Keys and API's\n\nAre you sure??", f"Uninstall {AppName}", buttons=[
                                        "Uninstall", "Don't Uninstall"])
                    if choice == "Uninstall":
                        res = DeleteAppConfig(AppName)
                        print(res)
                        if res == "Done":
                            connection = sqlite3.connect('AutoPoster.db')
                            cursor = connection.cursor()
                            cursor.execute(f'update Apps set isInstalled = "No" where Platform = "{AppName}"')
                            connection.commit()
                            connection.close()
                        else:
                            exit()
        root.destroy()


    root = Tk()
    root.geometry("700x500")
    root.title("App Management")
    root.resizable(height=False, width=False)

    textLabel = Label(root, text="App Management")
    textLabel.config(font=(20))
    textLabel.place(x=270, y=20)

    canvas = Canvas(root, width=600, height=400)
    frame = Frame(canvas)
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)

    for App in Apps:
        AppLabel = Label(frame, text=App[0], height=5)
        AppLabel.grid()
        Labelf = Message(frame, text=App[2], width=300)
        Labelf.grid(row=tempPlace, padx=5)
        if App[1] == 'No':
            Button(frame, command=lambda m=App[0]: CreateConfig(m, True),
                   text="Install with Guide").grid(row=tempPlacee, column=1, padx=(90, 0))
            Button(frame, command=lambda m=App[0]: CreateConfig(m),
                   text="Install").grid(row=tempPlacee, column=2)
        elif App[1] == "Yes":
            Button(frame, command=lambda m=App[0]: CreateConfig(m),
                   text="Uninstall").grid(row=tempPlacee, column=2)
            if App[0] == "Twitter":
                Button(frame, command=lambda m=App[0]: AddHashtag(),
                    text="Add Hashtags").grid(row=tempPlacee, column=1, padx=(90, 0))
            if App[0] == "Discord":
                Button(frame, command=lambda m=App[0]: AddChannel(),
                    text="Add Channels").grid(row=tempPlacee, column=1, padx=(90, 0))
            if App[0] == "Instagram":
                Button(frame, command=lambda m=App[0]: AddChannel(),
                    text="Add Accounts").grid(row=tempPlacee, column=1, padx=(90, 0))

        tempPlace += 2
        tempPlacee += 2

    canvas.create_window(0, 0, anchor='nw', window=frame, width=600)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                    yscrollcommand=scroll_y.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    canvas.focus_set()
    canvas.place(x=50, y=50)

    root.mainloop()

# getApps()