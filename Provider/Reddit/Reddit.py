import json
import os
import random
import socket
import sys
import webbrowser
import pyperclip as clip
import praw
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pymsgbox as pg


def GetRedditTags():
    currentPath = os.getcwd()
    path = os.path.join(currentPath, "Provider", "Reddit")
    os.chdir(path)
    with open("reddit.json", "r") as f:
        creds = json.load(f)
    os.chdir(currentPath)
    reddit = praw.Reddit(client_id=creds['client_id'],client_secret=creds['client_secret'],user_agent=creds['user_agent'],redirect_uri=creds['redirect_uri'],refresh_token=creds['refresh_token'])
    my_subs = [subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
    my_subs.sort()
    return my_subs


def GetRedditSub(options: list):
    root = Tk()
    root.config(width=500, height=len(options)*10)
    root.title("Select the Subreddits")
    root.geometry(f"500x500")

    optionCheckBox = {f"{options[0]}": IntVar()}
    for i in options:
        if i != options[0]:
            optionCheckBox[f"{i}"] = IntVar()

    def show():
        overallText = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                overallText += f"{key}+"
        clip.copy(overallText)
        root.destroy()
    text = ScrolledText(root, width=58, height=25)
    text.place(x=10, y=20)
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))
    Button(root, text="Next", command=show).place(x=230, y=440)
    label = Label(root, text=" ")
    label.pack()
    root.mainloop()

def PostOnReddit(title: str, subReddits: str, message: str, pathOfImage: str):
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Reddit")
    os.chdir(pathDir)
    with open("reddit.json", 'r') as f:
        creds = json.load(f)
    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token'])
    try:
        with open("bannedSubreddits.txt", 'r') as f:
            pass
    except FileNotFoundError:
        with open("bannedSubreddits.txt", 'a') as f:
            f.write("announcements")
    finally:
        with open("bannedSubreddits.txt", 'r') as f:
            subreds = f.readlines()
    for i in subReddits:
        subreddit = reddit.subreddit(i)
        reddit.validate_on_submit = True
        if f"{i}\n" not in subreds:
            try:
                if len(message) > 0:
                    subreddit.submit(title, selftext=message)
                else:
                    subreddit.submit_image(title, pathOfImage)
                print(f"Successfully Posted in {i}")
            except:
                with open("bannedSubreddits.txt", "a") as f:
                    f.write(f"{i}\n")
        else:
            print(f"Skipped Sub Reddit {i} because it is BlackListed")
    os.chdir(currentPath)


def Upload(title: str, message: str, pathOfImage: str):
    GetRedditSub(GetRedditTags())
    subReddits = str(clip.paste()).split("+")[:-1]
    PostOnReddit(title=title, subReddits=subReddits,
                 message=message, pathOfImage=pathOfImage)
    
def CreateRedditConfig():
    pg.alert("Create a New App from Reddit Apps Dashboard for this particular BOT.\n\nThe Link for that is https://www.reddit.com/prefs/apps", "Creating Reddit App")
    currentPath = os.getcwd()
    with open('config.json', 'r') as f:
        config = json.load(f)
    pathDir = os.path.join("Provider", "Reddit")
    os.chdir(pathDir)
    pg.alert("Your App Configuration should match something like this.\n\nApp type : Script\nAbout URL : http://localhost:8080\nredirect URI : http://localhost:8080", "Creating Reddit App")
    clientID = pg.prompt("Enter the Client ID ( Which is just below the Bot Name on Reddit Dev Dashboard )", "Collecting Client ID")
    clientSecret = pg.prompt("Enter the Client Secret", "Collecting Client Secret")
    refreshToken = main(clientID, clientSecret)
    if refreshToken != 1:
        dataSet = {
            "client_id": clientID,
            "client_secret": clientSecret,
            "user_agent": config["BotName"],
            "redirect_uri": "http://localhost:8080",
            "refresh_token": refreshToken
        }
        with open("reddit.json", 'w') as f:
            json.dump(dataSet, f, indent=4)
        os.chdir(currentPath)
        return "Done"
    else:
        pg.alert(
            "There was some Error in Authentication.\n\nPlease Try again", config["BotName"])
        os.chdir(currentPath)
        return "Error"


def receive_connection():
    """Wait for and then return a connected socket..
 
    Opens a TCP connection on port 8080, and waits for a single client.
 
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()


def main(clientID, ClientSecret):
    """Provide the program's entry point when directly executed."""
    print(
        "Go here while logged into the account you want to create a token for: "
        "https://www.reddit.com/prefs/apps/"
    )
    print(
        "Click the create an app button. Put something in the name field and select the"
        " script radio button."
    )
    print("Put http://localhost:8080 in the redirect uri field and click create app")
    client_id = clientID
    client_secret = ClientSecret
    # client_id = pg.prompt(
    #     "Enter the client ID, it's the line just under Personal use script at the top: ",
    #     "Enter the client ID, it's the line just under Personal use script at the top: "
    # )
    # client_secret = pg.prompt(
    #     "Enter the client secret, it's the line next to secret: ",
    #     "Enter the client secret, it's the line next to secret: ")
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

def DeleteRedditConfig():
    currentPath = os.getcwd()
    pathDir = os.path.join("Provider", "Reddit")
    os.chdir(pathDir)
    with open("reddit.json", 'w') as f:
        f.write("")
    os.chdir(currentPath)
    return "Done"


# main("H16YRr4yoRokEXkib96_cg", "rTD0tzRFMAcwRmXdF4b8NOkYToEGuQ")
