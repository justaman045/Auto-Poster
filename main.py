import pymsgbox as pg
from Provider.DataBase.DataBase import DataBase
from components.App.AppManagement import getApps
import components.Post.Post
import sqlite3
from BotVersion import BotVersion as version

BotVersion = version

connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
DataBase.CheckOrCreateDefault()

config = cursor.execute('select * from "Bot Config"').fetchall()
connection.close()

def startTheBot():
    BotName = config[0][0]
    choice = pg.confirm(BotName, BotName,
               buttons=["Post", "App Management", "Promote"])
    if choice == "Post":
        components.Post.Post.Post()
    elif choice == "App Management":
        try:
            getApps()
        finally:
            startTheBot()
    elif choice == 'Promote':
        pass
    else:
        exit()

startTheBot()