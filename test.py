import tkinter as tk
import tkinter.font as tkFont


class App:
    def __init__(self, root):
        #setting title
        root.title("BotName")
        #setting window size
        width = 345
        height = 220
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_2 = tk.Button(root)
        GButton_2["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times', size=10)
        GButton_2["font"] = ft
        GButton_2["fg"] = "#000000"
        GButton_2["justify"] = "center"
        GButton_2["text"] = "Post"
        GButton_2.place(x=30, y=160, width=70, height=25)
        GButton_2["command"] = self.GButton_2_command

        GButton_890 = tk.Button(root)
        GButton_890["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times', size=10)
        GButton_890["font"] = ft
        GButton_890["fg"] = "#000000"
        GButton_890["justify"] = "center"
        GButton_890["text"] = "App Management"
        GButton_890.place(x=200, y=150, width=121, height=44)
        GButton_890["command"] = self.GButton_890_command

        GLabel_43 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=38)
        GLabel_43["font"] = ft
        GLabel_43["fg"] = "#333333"
        GLabel_43["justify"] = "center"
        GLabel_43["text"] = "BotName"
        GLabel_43.place(x=80, y=60, width=172, height=75)

    def GButton_2_command(self):
        print("command")

    def GButton_890_command(self):
        print("command")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
