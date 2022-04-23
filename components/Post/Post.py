import pyperclip as clip
from Provider.Reddit.Reddit import Upload

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
    Post, Image = GetPostandImage()
    PlatformsToUpload = GetPlatforms()
    PlatformsToUploadImages = GetPlatformsImages()
    for i in PlatformsToUpload:
        if i == "Reddit":
            Upload()
        if i == "Twitter":
            print("Twitter")
