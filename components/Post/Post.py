from email import message
import pyperclip as clip
from Provider.Reddit.Reddit import Upload
import pymsgbox as pg

from components.GraphicalElements.PostBox import PlatformsToUpload, PlatformsToUploadImages, PostBox

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
        PlatformsToUpload = GetPlatforms()
        PlatformsToUploadImages = GetPlatformsImages()
    except:
        exit()
    for i in PlatformsToUpload:
        if i == "Reddit":
            title = pg.prompt("Enter the Title for Reddit", "Enter the title for Reddit")
            if "Reddit" in PlatformsToUploadImages:
                if len(Post) != 0 and Image != "":
                    choice = pg.confirm("Can't Upload Image and Post at same time on Reddit ( Beyond the Rules of Reddit )", "Error", buttons=[
                                        "Disable Post Text", "Disable Image Upload"])
                    if choice == "Disable Post Text":
                        Upload(title=title, message="", pathOfImage=Image)
                    elif choice == "Disable Image Upload":
                        Upload(title=title, message=Post, pathOfImage="")
            else:
                Upload(title=title, message=Post, pathOfImage="")
        if i == "Twitter":
            print("Twitter")
