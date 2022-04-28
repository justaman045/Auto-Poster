import json
import pymsgbox as pg
import pyperclip as clip



with open("config.json", 'r') as f:
    config = json.load(f)


def APISetup():
    pg.alert(
        f"Generate your Twitter App API Keys through which {config['BotName']} will communicate to Twitter. \n\nYou can Generate them through this link : https://developer.twitter.com/en/portal/projects-and-apps", config['BotName'])
    choice = pg.confirm(
        "Would you want to copy the link which was previously showed them to you??", config['BotName'], buttons=['Copy', "Don't Copy"])
    if str(choice).lower() == 'copy':
        clip.copy("https://developer.twitter.com/en/portal/projects-and-apps")
    elif str(choice).lower() == "don't copy":
        pass
    else:
        exit()
    pg.alert(f"Select Create App in that page after logging in and Give the Same name as this bot : {config['BotName']}",
             config['BotName'])
    pg.alert(
        "Now Click on the App Dashboard and go to the Keys and Token's Section and then create Access Token and Secret for your account", config['BotName'])
    Consumer_Key = pg.prompt("Enter the API Key Here : ", config['BotName'])
    Consumer_Secret = pg.prompt("Enter the API Key Secret Here : ", config['BotName'])
    Access_Token = pg.prompt("Enter the Access Token Here : ", config['BotName'])
    Access_Token_Secret = pg.prompt("Enter the Access Token Secret Here : ", config['BotName'])
    pg.alert("Now go on the Setting Tab of the App and Setup the User Authentication Settings and select OAuth 1.0a and give the App Permissions which ever you want from \nRead and Write \nRead and Write and Direct Message ( Recommended )\n and provide callback URI as http://localhost:8080/ and Website as ", )
    

pg.alert("""Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.""", "BOT")
