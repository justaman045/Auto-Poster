import os


try:
    import pymsgbox as pg
    from Provider.DataBase.DataBase import DataBase
    import sqlite3
    from BotVersion import BotVersion as version
except ModuleNotFoundError:
    os.system(f'pip install -r requirements.txt')
    os.system(f'python -m pip install --upgrade pip')
    print("\n\n\n\nPlease Restart this Software\n\n\n\nThanks for your Co-operation")
    exit()

BotVersion = version

connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
DataBase.CheckOrCreateDefault()
import components.Post.Post
from components.App.AppManagement import getApps

config = cursor.execute('select * from "Bot Config"').fetchall()
connection.close()

def startTheBot():
    BotName = config[0][0]
    choice = pg.confirm(BotName, BotName,
               buttons=["Post", "App Management"])
    if choice == "Post":
        components.Post.Post.Post()
    elif choice == "App Management":
        try:
            getApps()
        finally:
            startTheBot()
    else:
        exit()

startTheBot()