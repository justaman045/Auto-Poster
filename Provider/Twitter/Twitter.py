import json
import os
import sqlite3
import pymsgbox as pg
import pyperclip as clip
import tweepy


def APISetup():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    pg.alert(
        f"Generate your Twitter App API Keys through which {config[0]} will communicate to Twitter. \n\nYou can Generate them through this link : https://developer.twitter.com/en/portal/projects-and-apps", config[0])
    choice = pg.confirm(
        "Would you want to copy the link which was previously showed them to you??", config[0], buttons=['Copy', "Don't Copy"])
    if str(choice).lower() == 'copy':
        clip.copy("https://developer.twitter.com/en/portal/projects-and-apps")
    elif str(choice).lower() == "don't copy":
        pass
    else:
        exit()
    pg.alert(f"Select Create App in that page after logging in and Give the Same name as this bot : {config[0]}",
             config[0])
    pg.alert(
        "Now Click on the App Dashboard and go to the Keys and Token's Section and then create Access Token and Secret for your account", config[0])
    pg.alert("Now go on the Setting Tab of the App and Setup the User Authentication Settings and select OAuth 1.0a and give the App Permissions which ever you want from \nRead and Write \nRead and Write and Direct Message ( Recommended )\n and provide callback URI as http://localhost:8080/ and Website as https://twitter.com", config[0])
    pg.alert("Now go on the Keys and Tokens Tab and regenerate API Key and Secret and Access Token and Secret and Enter those now in this Software", config[0])
    pg.alert("Do Make Sure that you have applied for Elevated Access in Twitter as if not you won't be able to Upload Images", config[0])
    pg.alert("It seems thay you might not have applied for the Elevated Access for Twitter Or Maybe not yet Updated in the Backend. Please Check after 5 minutes to Post", config[0])
    connection.close()

def InstallTwitter():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    Consumer_Key = pg.prompt("Enter the API Key Here : ", config[0])
    Consumer_Secret = pg.prompt("Enter the API Key Secret Here : ", config[0])
    Access_Token = pg.prompt("Enter the Access Token Here : ", config[0])
    Access_Token_Secret = pg.prompt("Enter the Access Token Secret Here : ", config[0])
    hashtags = pg.prompt("Enter the Hashtags with the format #{hashtag} #{Hashtag}", config[0])
    cursor.execute(
        f'create table if not exists Twitter ( Consumer_Key VarChar2, Consumer_Secret VarChar2, Access_Token VarChar2, Access_Token_Secret VarChar2, Hashtag Text )')
    connection.commit()
    cursor.execute(
        f'insert into Twitter values ( "{Consumer_Key}", "{Consumer_Secret}", "{Access_Token}", "{Access_Token_Secret}", "{hashtags}" )')
    cursor.execute(f'update Apps set isInstalled = "Yes" where Platform = "Twitter"')
    connection.commit()
    connection.close()
    return "Done"

def UnInstallTwitter():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    cursor.execute('drop table Twitter')
    connection.commit()
    connection.close()
    return "Done"


def UploadToTwitter(Post, Image):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    data = cursor.execute('select * from Twitter').fetchall()[0]

    auth = tweepy.OAuthHandler(
        data[0], data[1])
    auth.set_access_token(
        data[2], data[3])

    api = tweepy.API(auth)
    client = tweepy.Client(consumer_key=data[0], consumer_secret=data[1], access_token=data[2], access_token_secret=data[3])
    if Image != "" and len(Post) != 0:
        mediaID = api.media_upload(Image)
        client.create_tweet(text=Post, media_ids=[mediaID.media_id_string])
    elif len(Post) == 0 and Image != "":
        mediaID = api.media_upload(Image)
        client.create_tweet(media_ids=[mediaID.media_id_string])
    elif Image == "" and len(Post) != 0:
        client.create_tweet(text=Post)

    connection.close()
    

def AddHashtagsToPost(Post):
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    data = cursor.execute('select * from Twitter').fetchall()[0]
    connection.close()
    return f'{Post}\n\n{data[4]} #detop'

    

def AddHashtag():
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()
    data = cursor.execute('select * from Twitter').fetchall()[0]
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]
    new_Hashtags = pg.prompt("Edit/Add New Hashtags for Twitter", config[0], data[4])
    if new_Hashtags != None:
        overallHashtag = ""
        for i in str(new_Hashtags).split(" "):
            if len(i) != 0:
                if len(str(i[1:]).split("#")) == 2:
                    listStr = str(i[1:]).split("#")
                    overallHashtag += f'#{listStr[0]} #{listStr[1]}'
                else:
                    overallHashtag += f'{i} '
        cursor.execute(f'update Twitter set "Hashtag" = "{overallHashtag}" where "Hashtag" = "{data[4]}"')
        connection.commit()
    connection.close()