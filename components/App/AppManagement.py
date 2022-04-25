import json
from tkinter import *

def getApps():

    with open("installedApps.json", 'r') as f:
        Apps = json.load(f)
    tempPlace = 1
    tempPlacee = 0

    def CreateConfig(AppName):
        if AppName == 'Twitter':
            print("Twitter")


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
        Labelf = Label(frame, text="Some Deatils")
        Labelf.grid(row=tempPlace, padx=5)
        Button(frame, command=lambda m=i: CreateConfig(m), text="Install").grid(row=tempPlacee, column=1, padx=350)
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

getApps()