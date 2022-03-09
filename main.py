import facebook
import json
import praw
import tweepy
import pymsgbox as msgbox
import os

class UpdateToPlatforms():
    def __init__(self):
        with open('client_secret.json') as f:
            self.creds = json.load(f)
        self.message = msgbox.prompt("Enter the Message you want to Post : ")
        try:
            if len(self.message) < 1:
                self.message = None
        except TypeError:
            exit
        if self.message != None:
            self.postItOneReddit = msgbox.confirm(
                'Do you want to Post this on Reddit??', 'Do you want to Post this on Reddit??', buttons=["Yes", 'No'])
            self.postItOneFacebook = msgbox.confirm(
                'Do you want to Post this on Facebook??', 'Do you want to Post this on Facebook??', buttons=["Yes", 'No'])
            self.postItOneTwitter = msgbox.confirm(
                'Do you want to Post this on Twitter??', 'Do you want to Post this on Twitter??', buttons=["Yes", 'No'])
            self.postItOneInstagram = msgbox.confirm(
                'Do you want to Post this on Instagram??', 'Do you want to Post this on Instagram??', buttons=["Yes", 'No'])
            if self.postItOneInstagram == 'Yes':
                self.postToInstgram()
            if self.postItOneFacebook == 'Yes':
                self.postToFacebook()
            if self.postItOneTwitter == 'Yes':
                if len(self.message) <= 250:
                    self.hashtags = msgbox.prompt(
                        "Enter the Hashtags on Twitter : ")
                    if self.hashtags == None:
                        exit
                self.postToTwitter()
            if self.postItOneReddit == 'Yes':
                self.title = msgbox.prompt(
                    "Enter the Title on Reddit : ")
                if self.title == None:
                    exit
                self.postToReddit()


    def postToReddit(self):
        reddit = praw.Reddit(client_id=self.creds['client_id'],
                             client_secret=self.creds['client_secret'],
                             user_agent=self.creds['user_agent'],
                             redirect_uri=self.creds['redirect_uri'],
                             refresh_token=self.creds['refresh_token'])
        subreddits = str(self.creds["subreddits"]).split(",")
        for i in subreddits:
            print(i)
            subreddit = reddit.subreddit(i)
            subreddit.submit(self.title, selftext=self.message)

    def postToFacebook(self):
        page_access_token = self.creds["facebook_access_token"]
        graph = facebook.GraphAPI(page_access_token)
        facebook_page_id = self.creds["facebook_page_id"]
        graph.put_object(facebook_page_id, "feed", message=self.message)

    def postToTwitter(self):
        auth = tweepy.OAuthHandler(
            self.creds["Twitter_api_key"], self.creds["Twitter_api_key_secret"])
        auth.set_access_token(self.creds["Twitter_access_token"],
                              self.creds["Twitter_access_token_secret"])
        api = tweepy.API(auth)
        tweet = f"{self.message}\n\n {self.hashtags} #Python #DEVCommunity #bot"
        status = api.update_status(status=tweet)

    def postToInstgram(self):
        username = self.creds["instagram_username"]
        password = self.creds["instgram_password"]
        image = "temp.png"
        text = 'Deleting this Image in 2 Minutes as this is a test for my New Project'
        os.chdir(os.getcwd())
        os.system(f"instapy -u {username} -p {password} -f {image} -t '{text}'")


detop = UpdateToPlatforms()
