import json
import os
import re
import sys
from components.Module_Installer.main import InstallAllModules

try:
    import random
    import socket
    import sqlite3
    import webbrowser
    import pyperclip as clip
    import praw
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText
    import pymsgbox as pg
    from redvid import Downloader
    import urllib.request
    import requests
except ModuleNotFoundError:
    InstallAllModules()


# Get all the Subreddits which A User is into 
def GetRedditTags():

    # Creating Connection to DataBase 
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()

    # Executing a Query to fetch the reddit API keys 
    creds = cursor.execute('select * from Reddit').fetchall()[0]

    # Logging into Reddit using API 
    reddit = praw.Reddit(client_id=creds[0],
                         client_secret=creds[1],
                         user_agent=creds[2],
                         redirect_uri=creds[3],
                         refresh_token=creds[4])

    # Getting all the Subreddits with it's display Name and sorting it alphabetical order
    my_subs = [subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
    my_subs.sort()

    # Closing the Database connection and returning the Output 
    connection.close()
    return my_subs


# GUI to select and get the Subreddits to post in 
def GetRedditSub(options: list):

    # Creating base root window with some of its properties 
    root = Tk()
    root.config(width=500, height=len(options)*10)
    root.title("Select the Subreddits")
    root.geometry(f"500x500")
    root.resizable(width=False, height=False)

    # Creating an array of Variables to store the value of the selected checkbox 
    optionCheckBox = {f"{options[0]}": IntVar()}
    for i in options:
        if i != options[0]:
            optionCheckBox[f"{i}"] = IntVar()

    # onclick Button so that whenever the next button is clicked some operations can be performed 
    def show():
        overallText = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                overallText += f"{key}+"
        clip.copy(overallText)
        root.destroy()

    # Developing some base window and Painting the UI so that elements can be interactable with the users 
    text = ScrolledText(root, width=58, height=25)
    text.place(x=10, y=20)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))
    Button(root, text="Next", command=show).place(x=230, y=440)
    label = Label(root, text=" ")
    label.pack()

    # Running the Root window in a loop so that the user can have time to select his subreddits to post 
    root.mainloop()


# Function to Post on Reddit Recursivly 
def PostOnReddit(title: str, subReddits: str, message: str, pathOfImage: str, pathOfVideos: str):

    # Creating connection from the DataBase 
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()

    # get the Reddit API Keys from Reddit 
    creds = cursor.execute('select * from Reddit').fetchall()[0]

    # Login into the Reddit using API Keys 
    reddit = praw.Reddit(client_id=creds[0],
                         client_secret=creds[1],
                         user_agent=creds[2],
                         redirect_uri=creds[3],
                         refresh_token=creds[4])

    # If there is no table named BannedSubred then create one to store the Names of Banned Subreddits 
    cursor.execute(
        'create table if not exists "BannedSubred" ( "Subreddits" Text )')

    # If it is created then commit and save the DataBase 
    connection.commit()

    # Now fetch all the Data from the DataBase from the Table named BannedSubred 
    subreds = cursor.execute('select * from "BannedSubred"').fetchall()

    # Sort it like it is a list 
    subreds = [x[0] for x in subreds]

    # Select one subreddit at a time and then post on it 
    for i in subReddits:

        # Authenticate the Subreddit 
        subreddit = reddit.subreddit(i)

        # Make it Validated after submission 
        reddit.validate_on_submit = True

        # check if the subreddit is not avavialable in the Banned Subreddits List then proceed else print that it is BlackListed
        if i not in subreds:

            # If there is no text to post then post image else post text only 
            try:
                if len(message) > 0:
                    subreddit.submit(title, selftext=message)
                    pass
                elif pathOfImage != None or pathOfImage == "":
                    subreddit.submit_image(title, pathOfImage)
                    pass
                else:
                    subreddit.submit_video(title, pathOfVideos)

                # After Posting print the message that it has been posted else it might have been black listed 
                print(f"Successfully Posted in {i}")

            except:

                # If there is any kind of error then it is treated as Banned from Subreddit and it's name is then saved as Banned from Subreddit 
                cursor.execute(f'insert into "BannedSubred" values ( "{i}" )')
        else:

            # If the Particular subreddit is found in the list of Blacklisted Subreddit then nothing is done with it else to just print that it's blacklisted 
            print(f"Skipped Sub Reddit {i} because it is BlackListed")

    # Now Everything is done then just save and close the connection of the Database 
    connection.commit()
    connection.close()


# A Function which recives the particular Information from the Main Post Area and Posts eveything by calling the PostOnReddit function 
def Upload(title: str, message: str, pathOfImage: str, pathOfVideos: str, subReddits: str):

    # Call the PostOnReddit Function to Upload 
    PostOnReddit(title=title, subReddits=subReddits,
                 message=message, pathOfImage=pathOfImage, pathOfVideos=pathOfVideos)


# A Basic Guide to Install the Reddit Module 
def RedditGuideToInstall():
    pg.alert("Create a New App from Reddit Apps Dashboard for this particular BOT.\n\nThe Link for that is https://www.reddit.com/prefs/apps", "Creating Reddit App")
    pg.alert("Your App Configuration should match something like this.\n\nApp type : Script\nAbout URL : http://localhost:8080\nredirect URI : http://localhost:8080", "Creating Reddit App")

    
# Reddit Config Creation with the Reddit API and the DataBase
def CreateRedditConfig():

    # Creating the Connection with the Database 
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()

    # Query to fetch data from the DataBase 
    config = cursor.execute('select * from "Bot Config"').fetchall()[0]

    # Get the Input from the User for the Client ID if nothing entered then exit 
    clientID = pg.prompt("Enter the Client ID ( Which is just below the Bot Name on Reddit Dev Dashboard )", "Collecting Client ID")
    if clientID == None:
        exit()

    # Get the ClientSecret from the User if nothing entered then exit 
    clientSecret = pg.prompt("Enter the Client Secret", "Collecting Client Secret")
    if clientSecret == None:
        exit()

    # Get the Refresh Token from the Reddit Official Website 
    refreshToken = main(clientID, clientSecret)

    # If Refresh Token is succesfully caught then create a Reddit Table in DataBase and save the changes 
    if refreshToken != 1:

        # create the table named as Reddit 
        cursor.execute(f'create table if not exists Reddit ( ClientId VarChar2, ClientSecret VarChar2, UserAgent Text, redirectURI VarChar2, refreshToken VarChar2 )')

        # Insert the Values in it 
        cursor.execute(
            f'insert into Reddit values ( "{clientID}", "{clientSecret}", "{config[0]}", "http://localhost:8080", "{refreshToken}" )')
        
        # Update the Apps Table also so that it indicates that Reddit Module has been Installed 
        cursor.execute('UPDATE Apps SET isInstalled = "Yes" WHERE Platform = "Reddit"')

        # Commit and close the DataBase connection 
        connection.commit()
        connection.close()

        # Return the Done str so that rest of the things can be done 
        return "Done"
    else:

        # If there is any kind of error then tell the user that there is an error 
        pg.alert(
            "There was some Error in Authentication.\n\nPlease Try again", config["BotName"])
        return "Error"

# Functions to get the refresh token from Reddit 
def receive_connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()


def main(clientID, ClientSecret):
    client_id = clientID
    client_secret = ClientSecret
    commaScopes = 'all'

    if commaScopes.lower() == "all":
        scopes = ["*"]
    else:
        scopes = commaScopes.strip().split(",")

    reddit = praw.Reddit(
        client_id=client_id.strip(),
        client_secret=client_secret.strip(),
        redirect_uri="http://localhost:8080",
        user_agent="praw_refresh_token_example",
    )
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes, state, "permanent")
    webbrowser.open_new(url)
    sys.stdout.flush()

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected: {state} Received: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, f"Refresh token: {refresh_token}")
    return refresh_token


# Delete the Config of Reddit from the DataBase 
def DeleteRedditConfig():

    # Create the Connection from the DataBase 
    connection = sqlite3.connect('AutoPoster.db')
    cursor = connection.cursor()

    # Delete the Table from the Database Named Reddit 
    cursor.execute('drop table Reddit')

    # Close the connection and commit the changes 
    connection.commit()
    connection.close()

    # Return Done which indicates that the deleting of the API Keys was successful 
    return "Done"


def DownloadSavedVids():

    # open the config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    try:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
    except FileNotFoundError:
        CreateRedditConfig()
    finally:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)

    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token'])

    out_filename = 'alreadyDownloaded.txt'
    try:
        os.mkdir("Reddit_Saved_Vods")
    except:
        pass
    curretLoc = os.getcwd()
    os.chdir("Reddit_Saved_Vods")

    try:
        with open(f"{out_filename}.txt", 'r') as f:
            pass
    except FileNotFoundError:
        with open(f"{out_filename}.txt", 'w') as f:
            pass
    finally:
        with open(f"{out_filename}.txt", 'r') as f:
            urls = f.readlines()

    with open(out_filename, 'w') as out_file:
        for item in reddit.user.me().saved(limit=None):
            submission = reddit.submission(id=item.id)
            try:

                url = submission.url
                if f'{url}\n' not in urls:

                    if str(url).split(".")[len(str(url).split("."))-1] == "gifv" or str(url).split(".")[len(str(url).split("."))-1] == "gif" or str(url).split(".")[len(str(url).split("."))-1] == "jpg":
                        nameOfVid = f'{submission.title}.mp4'.replace(" ", "_")
                        urllib.request.urlretrieve(url, nameOfVid)

                    elif str(url).split('/')[2] == 'redgifs.com' or str(url).split('/')[2] == "www.redgifs.com":
                        redgif_id = re.match(r'.*/(.*?)/?$', url).group(1)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/90.0.4430.93 Safari/537.36',
                        }
                        content = requests.get(
                            f'https://api.redgifs.com/v2/gifs/{redgif_id}', headers=headers).json()
                        video = requests.get(
                            url=content['gif']["urls"]['hd'], headers=headers)
                        open(
                            f"{str(submission.title).replace(' ', '_').replace('.', '').replace(',', '').replace('?', '').replace('/', '')}.mp4", 'wb').write(video.content)

                    elif str(url).split('/')[2] == "v.redd.it":
                        downloadRedVid = Downloader(max_q=True)
                        downloadRedVid.url = url
                        downloadRedVid.download()
                    else:
                        print(
                            f'{url} got an error!! Please check if this is correct or not')

                    out_file.write(f'{url}\n')

            except BaseException as e:
                print(e)
