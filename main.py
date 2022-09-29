import os
from Provider.DataBase.DataBase import DataBase
from BotVersion import BotVersion as version
import sqlite3
from components.Module_Installer.main import InstallAllModules

try:
    import pymsgbox as pg
except ModuleNotFoundError:
    InstallAllModules()



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