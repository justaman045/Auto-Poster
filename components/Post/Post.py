import os

try:
    import sqlite3
    import pyperclip as clip
    from Provider.Discord.Discord import sendDiscordMessage
    from Provider.Instagram.Instagram import UploadTOIG
    from Provider.Reddit.Reddit import GetRedditSub, GetRedditTags, Upload
    import pymsgbox as pg
    from Provider.Twitter.Twitter import AddHashtagsToPost, UploadToTwitter

    from components.GraphicalElements.PostBox import MultiPurposeOptionBox, PlatformsToUpload, PlatformsToUploadImages, PostBox
except ModuleNotFoundError:
    os.system(f'pip install -r requirements.txt')
    os.system(f'python -m pip install --upgrade pip')
    print("\n\n\n\nPlease Restart this Software\n\n\n\nThanks for your Co-operation")
    exit()

connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
config = cursor.execute('select * from "Bot Config"').fetchall()[0]
connection.close()

def GetPostandImage():
    PostBox("Enter Your Post")
    Post, Image = str(clip.paste()).split("+")
    return Post, Image
    
def GetPlatforms(Image):
    PlatformsToUpload(Image)
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload


def GetPlatformsImages():
    PlatformsToUploadImages()
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload

def Post():
    Post = None
    Image = None
    PlatformsToUploadImagess = None
    PlatformsToUploads = None
    try:
        Post, Image = GetPostandImage()
        PlatformsToUploads = GetPlatforms(Image)
        if Image == "":
            PlatformsToUploadImagess = []
        else:
            PlatformsToUploadImagess = GetPlatformsImages()
    except:
        SystemExit()
    finally:
        if Post != None or Image != None:
            PostOnSocials(Post, Image, PlatformsToUploadImagess, PlatformsToUploads)
    

def PostOnSocials(Message, LocationOfImage, PlatformsToUploadImagess, PlatformsToUploads):
    channels = []
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
                GetRedditSub(GetRedditTags())
                subReddits = str(clip.paste()).split("+")[:-1]
            if i == "Twitter":
                if len(Message) < 270:
                    TwitterPost = AddHashtagsToPost(Message)
                else:
                    TwitterPost = Message
                toUpload.append(i)
            if i == 'Discord':
                toUpload.append(i)
                connection = sqlite3.connect('AutoPoster.db')
                cursor = connection.cursor()
                discord = cursor.execute('select * from Discord').fetchall()
                discordConfig = []
                for i in discord:
                    discordConfig.append(i[3])
                MultiPurposeOptionBox("Select on which Channels you want to send Message", discordConfig,
                                      "Discord App has been currupted in you local machine ( Please Re-install the app again from App Management )")
                channels = str(clip.paste()).split("+")
                channels = channels[:-1]
                connection.close()
            if i == 'Instagram':
                toUpload.append(i)
                connection = sqlite3.connect('AutoPoster.db')
                cursor = connection.cursor()
                ig = cursor.execute('select * from Instagram').fetchall()
                credConfig = []
                for i in ig:
                    credConfig.append(i[0])
                MultiPurposeOptionBox("Select on which Account you want to Upload Image", credConfig,
                                      "Instagram App has been currupted in you local machine ( Please Re-install the app again from App Management )")
                account = str(clip.paste()).split("+")
                accounts = account[:-1]
                connection.close()
    finally:
        if len(toUpload) == 0:
            pg.alert(
                "Status/Post/Tweet wasn't sent as Platform wasn't specified", config[0])
            exit()
        else:
            pg.alert(
                "Uploading Status/Post/Tweet to the Selected Platforms\n\nPlease Wait", config[0])
        if "Twitter" in toUpload:
            UploadToTwitter(TwitterPost, LocationOfImage)
        if "Discord" in toUpload:
            sendDiscordMessage(Message, LocationOfImage, discordConfig, channels)
        if "RedditDPT" in toUpload:
            Upload(title=title, message="",
                   pathOfImage=LocationOfImage)
        if "RedditDIU" in toUpload or "RedditNI" in toUpload:
            Upload(title=title, message=Message,
                   pathOfImage="", subReddits=subReddits)
        if "Instagram" in toUpload:
            UploadTOIG(LocationOfImage, Message, accounts)
        pg.alert("Sucessfully Uploaded the Tweet/Status to every Playform", config[0])
