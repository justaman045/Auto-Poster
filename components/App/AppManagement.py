import json
from tkinter import *
import pymsgbox as pg

from Provider.Reddit.Reddit import CreateRedditConfig, DeleteRedditConfig

def getApps():

    with open("installedApps.json", 'r') as f:
        Apps = json.load(f)
    tempPlace = 1
    tempPlacee = 0

    def CreateAppConfig(App):
        if App == 'Reddit':
            return CreateRedditConfig()

    def DeleteAppConfig(App):
        if App == 'Reddit':
            return DeleteRedditConfig()

    def CreateConfig(AppName):
        if Apps[AppName]["installed"] == "Yes":
            choice = pg.confirm(f"This will Uninstall {AppName} and Clear all the Application Keys and API's\n\nAre you sure??", f"Uninstall {AppName}", buttons=["Uninstall", "Don't Uninstall"])
            if choice == "Uninstall":
                res = DeleteAppConfig(AppName)
                if res == "Done":
                    Apps[AppName]["installed"] = "NO"
                    with open("installedApps.json", 'w') as f:
                        json.dump(Apps, f, indent=4)
                else:
                    exit()
            else:
                pg.alert(f"{AppName} hasn't been Uninstalled and you can still use it.", "UnInstall Aborted")
        elif Apps[i]["installed"] == "NO":
            res = CreateAppConfig(AppName)
            if res == "Done":
                Apps[AppName]["installed"] = "Yes"
                with open("installedApps.json", 'w') as f:
                    json.dump(Apps, f, indent=4)
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

    for i in Apps:
        AppLabel = Label(frame, text=i, height=5)
        AppLabel.grid()
        Labelf = Message(frame, text=Apps[i]["Detail"], width=300)
        Labelf.grid(row=tempPlace, padx=5)
        if Apps[i]["installed"] == 'NO':
            Button(frame, command=lambda m=i: CreateConfig(m),
                   text="Install").grid(row=tempPlacee, column=1, padx=130)
        elif Apps[i]["installed"] == "Yes":
            Button(frame, command=lambda m=i: CreateConfig(m),
                   text="Uninstall").grid(row=tempPlacee, column=1, padx=130)
        tempPlace += 2
        tempPlacee += 2

    canvas.create_window(0, 0, anchor='nw', window=frame, width=500)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                    yscrollcommand=scroll_y.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    canvas.focus_set()
    canvas.place(x=50, y=50)

    root.mainloop()

# getApps()