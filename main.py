from components.Inside_Tester.main import CheckForDevAccounts, InsideTester
from Provider.DataBase.DataBase import DataBase
from BotVersion import BotVersion as version
import sqlite3
from components.Module_Installer.main import InstallAllModules
from components.Update_Script.main import Update, checkUpdateAndUpdate
# import pymsgbox as pg

try:
    import pymsgbox as pg
except ModuleNotFoundError:
    InstallAllModules()

connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
DataBase.CheckOrCreateDefault()
checkUpdateAndUpdate()
CheckForDevAccounts()
import components.Post.Post
from components.App.AppManagement import getApps

config = cursor.execute('select * from "Bot Config"').fetchall()
connection.close()

def startTheBot():
    BotName = config[0][0]
    choice = pg.confirm(BotName, BotName,
               buttons=["Post", "Inside Tester", "App Management"])
    if choice == "Post":
        components.Post.Post.Post()
    elif choice == "App Management":
        try:
            getApps()
        finally:
            startTheBot()
    elif choice == "Inside Tester":
        try:
            InsideTester()
        finally:
            startTheBot()
    else:
        exit()

startTheBot()