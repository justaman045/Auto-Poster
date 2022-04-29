import json
import os
import pymsgbox as pg
import pyperclip as clip
import tweepy


def APISetup():
    with open("config.json", 'r') as f:
        config = json.load(f)
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
    pg.alert("Now go on the Setting Tab of the App and Setup the User Authentication Settings and select OAuth 1.0a and give the App Permissions which ever you want from \nRead and Write \nRead and Write and Direct Message ( Recommended )\n and provide callback URI as http://localhost:8080/ and Website as https://twitter.com", config["BotName"])
    pg.alert("Now go on the Keys and Tokens Tab and regenerate API Key and Secret and Access Token and Secret and Enter those now in this Software", config["BotName"])

def InstallTwitter():
    with open("config.json", 'r') as f:
        config = json.load(f)
    Consumer_Key = pg.prompt("Enter the API Key Here : ", config['BotName'])
    Consumer_Secret = pg.prompt("Enter the API Key Secret Here : ", config['BotName'])
    Access_Token = pg.prompt("Enter the Access Token Here : ", config['BotName'])
    Access_Token_Secret = pg.prompt("Enter the Access Token Secret Here : ", config['BotName'])
    currentPath = os.getcwd()
    with open('config.json', 'r') as f:
        config = json.load(f)
    pathDir = os.path.join("Provider", "Twitter")
    os.chdir(pathDir)
    with open("twitter.json", 'w') as f:
        dataSet = {
            "Consumer_Key": Consumer_Key,
            "Consumer_Secret": Consumer_Secret,
            "Access_Token": Access_Token,
            "Access_Token_Secret": Access_Token_Secret
        }
        json.dump(dataSet, f, indent=4)
    os.chdir(currentPath)
    return "Done"

def UnInstallTwitter():
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Twitter")
    os.chdir(pathDir)
    with open("twitter.json", 'w') as f:
        f.write("")
    os.chdir(currentPath)
    return "Done"


def UploadToTwitter(Post, Image):
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Twitter")
    os.chdir(pathDir)
    with open("twitter.json", 'r') as f:
        twitterData = json.load(f)

    auth = tweepy.OAuthHandler(
        twitterData["Consumer_Key"], twitterData["Consumer_Secret"])
    auth.set_access_token(
        twitterData["Access_Token"], twitterData["Access_Token_Secret"])

    api = tweepy.API(auth)
    if Image != "" and len(Post) != 0:
        print("Update Media with Status")
        api.update_status_with_media(Post, Image)
    elif len(Post) == 0 and Image != "":
        print("Upload Media")
        api.media_upload(file=Image)
    elif Image == "" and len(Post) != 0:
        print("Update Status")
        api.update_status(Post)

    os.chdir(currentPath)

def AddHashtags(Post):
    with open("config.json", 'r') as f:
        config = json.load(f)
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Twitter")
    os.chdir(pathDir)
    try:
        with open("Hashtags.txt", 'r') as f:
            pass
    except:
        with open("Hashtags.txt", 'w') as f:
            hashtags = pg.prompt(
                "Enter The Hashtags you want to Enter at the end of your Tweets seperated with spaces", config['BotName'])
            hashtags = str(hashtags).split(" ")
            hashtag = ""
            for i in hashtags:
                hashtag += f'{i} '
            hashtags = f'{hashtag}'
            f.write(hashtags)
    finally:
        with open("Hashtags.txt", 'r') as f:
            hashtags = f.read()
            print(len(Post))
            os.chdir(currentPath)
            return f'{Post}\n\n{hashtags}#detop'


# print(AddHashtags(
#     "Enter The Hashtags you want to Enter The Hashtags you wantacesEnter The Hashtags you want to of your Tweets seperated with spacesEnter at the end of your Tweets seperated with spacesEnter The Hashtags you want to Enter at the end of your Tweets seperated with spaces"))
