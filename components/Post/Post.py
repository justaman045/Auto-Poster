from components.Module_Installer.main import InstallAllModules
from Provider.Discord.Discord import sendDiscordMessage
from Provider.Instagram.Instagram import UploadTOIG
from Provider.Reddit.Reddit import GetRedditSub, GetRedditTags, Upload
from Provider.Twitter.Twitter import AddHashtagsToPost, UploadToTwitter
from components.GraphicalElements.PostBox import MultiPurposeOptionBox, PlatformsToUpload, PlatformsToUploadImages, PostBox

try:
    import sqlite3
    import pyperclip as clip
    import pymsgbox as pg
except ModuleNotFoundError:
    InstallAllModules()

# get the basics of bot e.g. name of bot, configuration 
connection = sqlite3.connect('AutoPoster.db')
cursor = connection.cursor()
config = cursor.execute('select * from "Bot Config"').fetchall()[0]
connection.close()

# Get the Image and videos location and the text of the post
def GetPostandImage():

    # call the dialogue box to write a custom text/post 
    PostBox("Enter Your Post")

    # Get the text locations and post text 
    Post, Image, Videos = str(clip.paste()).split("+")
    return Post, Image, Videos
    
# Get all the Installed Platforms 
def GetPlatforms(length):

    # Get the Installed Apps 
    PlatformsToUpload(length)

    # Get the Platforms Names as a list in a variable 
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload

# Get the Platform Image locations 
def GetPlatformsImages():

    # Create a Dialogue box with all the platforms that are enabled to upload Images in that 
    PlatformsToUploadImages()

    # Get the Platforms in the Variable as a list 
    PlatformsUpload = str(clip.paste()).split("+")[:-1]
    return PlatformsUpload

def Post():
    # Declaring Blank Variables to use it in future 
    Post = None
    Image = None
    Videos = None

    try:
        # Get the Post Text and Image Location 
        Post, Image, Videos = GetPostandImage()

        # Get the platforms on which Images and Videos locations 
        PlatformsToUploads = GetPlatforms(len(Image))

        # Double Check if the values are blank the get the locations again
        if Image == "" or Videos == "" or Image == None or Videos == None:
            PlatformsToUploadImagess = []
        else:
            PlatformsToUploadImagess = GetPlatformsImages()
    except:

        # Exit if any other issue occurs
        SystemExit()
    finally:

        # If Everything is done correctly then have a safty check and then perform the actions
        if Post != None or Image != None or Videos != None or Post != "" or Image != "" or Videos != "":
            PostOnSocials(Post, Image, Videos, PlatformsToUploadImagess, PlatformsToUploads)
    

# Post to Social Media 
def PostOnSocials(Message, LocationOfImage, LocationOfVideos, PlatformsToUploadImagess, PlatformsToUploads):

    # Creating blank lists to use in future 
    channels = []
    toUpload = []

    # Filter and Call the specific methods to upload on it 
    try:
        for i in PlatformsToUploads:
            if i == "Reddit":
                title = pg.prompt("Enter the Title for Reddit",
                                "Enter the title for Reddit")
                if "Reddit" in PlatformsToUploadImagess:
                    if len(Message) != 0 and LocationOfImage != "" or LocationOfVideos != None:
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

            # If the Platform selected is Twitter then perform this action 
            if i == "Twitter":

                # If the Message/Post is less than 270 charecters then add the hashtags to the text post 
                if len(Message) < 270:

                    # Add the hashtags and return the text post in a variable 
                    TwitterPost = AddHashtagsToPost(Message)

                else:

                    # Append the Hashtags to the Twitter Posts 
                    TwitterPost = Message

                # Update the toUpload list to state that the twitter post is ready to be uploaded 
                toUpload.append(i)

            # Perform the specific actions if the selected platform is Discord 
            if i == 'Discord':

                # Append the platform in the toUpload list to indicate that the platform is ready to upload all the posts on the channels 
                toUpload.append(i)

                # Making a DB connection to fetch the channels 
                connection = sqlite3.connect('AutoPoster.db')
                cursor = connection.cursor()
                discord = cursor.execute('select * from Discord').fetchall()

                # Creaating a Discord Config variable to use in future 
                discordConfig = []

                # If the Selected channel is avaiable in the discord config then list it in the postbox 
                for i in discord:
                    discordConfig.append(i[3])
                
                # Make the user to select the channels in which the auto Poster have to Upload the PostBox 
                MultiPurposeOptionBox("Select on which Channels you want to send Message", discordConfig,
                                      "Discord App has been currupted in you local machine ( Please Re-install the app again from App Management )")
                
                # Get the Channels which the user have selected and store them in the list 
                channels = str(clip.paste()).split("+")

                # Remove the last channel as it have a un-necessary stuff in the last item 
                channels = channels[:-1]

                # close the database connection which we created at the start 
                connection.close()


            # If Selected Platform is Instagram then perform these actions   
            if i == 'Instagram':

                # Append the selected platform to confirm the upload to happen 
                toUpload.append(i)

                # make connection to DataBase and get the Instagram Details from DataBase 
                connection = sqlite3.connect('AutoPoster.db')
                cursor = connection.cursor()
                ig = cursor.execute('select * from Instagram').fetchall()

                # Create a blank variable to use it for further use 
                credConfig = []

                # Get all the Configured Instagram Accounts to make user to select accounts 
                for i in ig:
                    credConfig.append(i[0])

                # Ask user to select on which Instagram account he wants to Upload 
                MultiPurposeOptionBox("Select on which Account you want to Upload Image", credConfig,
                                      "Instagram App has been currupted in you local machine ( Please Re-install the app again from App Management )")
                
                # Store the user choice in a list after removing the last item as it's a extra useless item 
                account = str(clip.paste()).split("+")
                accounts = account[:-1]

                # close the Database connection 
                connection.close()

    # After Performing all the platform specific actions finally upload the posts on user dezired platform using the list we were creating 
    finally:

        # If the list is empty exit straight away
        if len(toUpload) == 0:
            pg.alert(
                "Status/Post/Tweet wasn't sent as Platform wasn't specified", config[0])
            exit()

        # else display a tkinter msg that the posts are being uploaded 
        else:
            pg.alert(
                "Uploading Status/Post/Tweet to the Selected Platforms\n\nPlease Wait", config[0])
            
        # if Twitter is in the list then upload the posts with the performed actions to twitter 
        if "Twitter" in toUpload:
            UploadToTwitter(TwitterPost, LocationOfImage, LocationOfVideos)

        # If Discord is in the list then upload the posts with the performed actions to Discord 
        if "Discord" in toUpload:
            sendDiscordMessage(Message, LocationOfImage, LocationOfVideos, discordConfig, channels)

        # If Reddit is the the 
        if "RedditDPT" in toUpload:
            Upload(title=title, message="",
                   pathOfImage=LocationOfImage, pathOfVideos=LocationOfVideos)
        if "RedditDIU" in toUpload or "RedditNI" in toUpload:
            Upload(title=title, message=Message,
                   pathOfImage="", subReddits=subReddits)
        if "Instagram" in toUpload:
            UploadTOIG(LocationOfImage, LocationOfVideos, Message, accounts)
        pg.alert("Sucessfully Uploaded the Tweet/Status to every Playform", config[0])
