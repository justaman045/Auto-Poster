import os
import sqlite3
import pymsgbox as pg

from BotVersion import BotVersion as version

BotVersion = version

class DataBase:

    def CheckOrCreateDefault():
        connection = sqlite3.connect('AutoPoster.db')
        cursor = connection.cursor()
        cursor.execute('create table if not exists "Bot Config" ( "Bot Name" Text, Version VarChar2 )')
        cursor.execute('create table if not exists Apps ( Platform Text, isInstalled Text, "About Platform" text )')
        Data = cursor.execute('select * from Apps').fetchall()
        if len(Data) == 0:
            SqlStatements = [
                "insert into Apps values ( 'Reddit', 'No', 'Post on Reddit a Social Media Platform based on sub-reddits ( Communities ) without even opening Reddit' )",
                "insert into Apps values ( 'Twitter', 'No', 'Post on Twitter a Social Media Platform will just tweet.' )",
                "insert into Apps values ( 'Discord', 'No', 'Send Messages to Discord using this Bot with ease' )",
            ]
            for i in SqlStatements:
                cursor.execute(i)
            connection.commit()
        Data = cursor.execute('select * from "Bot Config"').fetchall()
        if len(Data) == 0:
            BotName = pg.prompt("Enter the Bot Name",
                                "Enter the Bot Name", f"{os.getlogin()}'s Bot")
            SqlStatements = [
                f"insert into 'Bot Config' values ( '{BotName}', '{BotVersion}' )",
            ]
            for i in SqlStatements:
                cursor.execute(i)
            connection.commit()
        
