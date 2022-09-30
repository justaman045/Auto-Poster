import sqlite3

from components.Module_Installer.main import InstallAllModules

try:
    import pymsgbox as pg
except ModuleNotFoundError:
    InstallAllModules()

DevAccounts = ['Instagram']

def InsideTester():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    devaccounts = cursor.execute("select * from 'Dev Accounts'").fetchall()
    DevAccountsEnabled, DevAccountsNotEnabled = [], []
    for i in devaccounts:
        if i[1] == "True":
            DevAccountsEnabled.append(i[0])
        else:
            DevAccountsNotEnabled.append(i[0])
    choice = pg.confirm("This will enable Tester Mode which can be unstable.",
                        "Enable Testing Mode", buttons=['Enable Tester Mode', 'Disable Tester Mode', "Naah! Go Back"])
    if choice == "Enable Tester Mode":
        if len(DevAccountsEnabled) == len(DevAccounts):
            pg.alert("All of the Dev Features are Enabled")
        else:
            feature = pg.confirm("Select Which Feature to Enable in Testing Mode",
                                 "Select Feature to Enable", buttons=DevAccountsNotEnabled)
            cursor.execute(
                f"update 'Dev Accounts' set DevFeature='True' where Platform='{feature}'")
            connection.commit()
    if choice == "Disable Tester Mode":
        if len(DevAccountsNotEnabled) == len(DevAccounts):
            pg.alert("All of the Dev Features are Disabled")
        else:
            feature = pg.confirm("Select Which Feature to Disbale in Testing Mode",
                                 "Select Feature to Disbale", buttons=DevAccountsEnabled)
            cursor.execute(
                f"update 'Dev Accounts' set DevFeature='False' where Platform='{feature}'")
            connection.commit()

def NoDevFeature(appName):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    devaccounts = cursor.execute("select * from 'Dev Accounts'").fetchall()
    DevAccountsEnabled, DevAccountsNotEnabled = [], []
    for i in devaccounts:
        if i[1] == "True":
            DevAccountsEnabled.append(i[0])
        else:
            DevAccountsNotEnabled.append(i[0])
    if appName in DevAccountsEnabled:
        return True
    if appName in DevAccountsNotEnabled:
        return False
    return True

def CheckForDevAccounts():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    devaccounts = cursor.execute(
        'create table if not exists "Dev Accounts" ( Platform Text, DevFeature Text )')
    connection.commit()
    devaccounts = cursor.execute("select * from 'Dev Accounts'").fetchall()
    try:
        removedApps = list(set(devaccounts[0]) - set(DevAccounts))
    except IndexError:
        removedApps = []
    try:
        newlyAddedApps = list(set(DevAccounts) - set(devaccounts[0]))
    except IndexError:
        newlyAddedApps = DevAccounts
    if len(newlyAddedApps) != 0:
        for i in newlyAddedApps:
            cursor.execute(f"insert into 'Dev Accounts' values ( '{i}', 'False' )")
            connection.commit()
    if len(removedApps) != 0:
        for i in removedApps:
            cursor.execute(f"delete from 'Dev Accounts' where Platform='{i}'")
            connection.commit()
