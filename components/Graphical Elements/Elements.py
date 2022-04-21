from tkinter import *
from tkinter import ttk

root = Tk()

def Buttons():
    def PrintHello():
        print("Hello World")


    ttk.Button(root, text="Somthing Recived",
            command=PrintHello).grid(row=0, column=0)

    root.mainloop()

Buttons()