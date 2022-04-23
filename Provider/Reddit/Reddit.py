import json
import os
import pyperclip as clip
import praw
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def GetRedditTags():
    currentPath = os.getcwd()
    path = os.path.join(currentPath, "Provider", "Reddit")
    os.chdir(path)
    with open("reddit.json", "r") as f:
        creds = json.load(f)
    os.chdir(currentPath)
    reddit = praw.Reddit(client_id=creds['client_id'],client_secret=creds['client_secret'],user_agent=creds['user_agent'],redirect_uri=creds['redirect_uri'],refresh_token=creds['refresh_token'])
    my_subs = [subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
    my_subs.sort()
    return my_subs


def GetRedditSub(options: list):
    root = Tk()
    root.config(width=500, height=len(options)*10)
    root.title("Select the Subreddits")
    root.geometry(f"500x500")

    optionCheckBox = {f"{options[0]}": IntVar()}
    for i in options:
        if i != options[0]:
            optionCheckBox[f"{i}"] = IntVar()

    def show():
        overallText = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                overallText += f"{key}+"
        clip.copy(overallText)
        root.destroy()
    text = ScrolledText(root, width=58, height=25)
    text.place(x=10, y=20)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))
    Button(root, text="Next", command=show).place(x=230, y=440)
    label = Label(root, text=" ")
    label.pack()
    root.mainloop()


def Upload():
    GetRedditSub(["Hello", "World"])
