import json
import pyperclip as clip
from Provider.Discord.Discord import sendDiscordMessage
from Provider.Reddit.Reddit import Upload
import pymsgbox as pg
from Provider.Twitter.Twitter import AddHashtags, UploadToTwitter

from components.GraphicalElements.PostBox import PlatformsToUpload, PlatformsToUploadImages, PostBox

with open("config.json", 'r') as f:
    config = json.load(f)

def GetPostandImage():
    PostBox("Enter Your Post")
    Post, Image = str(clip.paste()).split("+")
    return Post, Image
    
def GetPlatforms():
    PlatformsToUpload()
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload


def GetPlatformsImages():
    PlatformsToUploadImages()
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload

def Post():
    try:
        Post, Image = GetPostandImage()
        PlatformsToUploads = GetPlatforms()
        if Image == "":
            PlatformsToUploadImagess = []
        else:
            PlatformsToUploadImagess = GetPlatformsImages()
    except:
        exit()
    finally:
        PostOnSocials(Post, Image, PlatformsToUploadImagess, PlatformsToUploads)
    

def PostOnSocials(Message, LocationOfImage, PlatformsToUploadImagess, PlatformsToUploads):
    toUpload = []
    try:
        for i in PlatformsToUploads:
            if i == "Reddit":
                title = pg.prompt("Enter the Title for Reddit",
                                "Enter the title for Reddit")
                if "Reddit" in PlatformsToUploadImagess:
                    if len(Message) != 0 and LocationOfImage != "":
                        choice = pg.confirm("Can't Upload Image and Post at same time on Reddit ( Beyond the Rules of Reddit )", "Error", buttons=[
                                            "Disable Post Text", "Disable Image Upload"])
                        if choice == "Disable Post Text":
                            toUpload.append(f'{i}DPT')
                        elif choice == "Disable Image Upload":
                            toUpload.append(f'{i}DIU')
                else:
                    toUpload.append(f'{i}NI')
            if i == "Twitter":
                if len(Message) < 270:
                    TwitterPost = AddHashtags(Message)
                else:
                    TwitterPost = Message
                toUpload.append(i)
            if i == 'Discord':
                toUpload.append(i)
    finally:
        pg.alert(
            "Sucessfully Uploaded the Tweet/Status to every Playform", config["BotName"])
        if "Twitter" in toUpload:
            UploadToTwitter(TwitterPost, LocationOfImage)
        if "Discord" in toUpload:
            sendDiscordMessage(Message)
        if "RedditDPT" in toUpload:
            Upload(title=title, message="",
                   pathOfImage=LocationOfImage)
        if "RedditDIU" in toUpload or "RedditNI" in toUpload:
            Upload(title=title, message=Message, pathOfImage="")
