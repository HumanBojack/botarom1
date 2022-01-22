import os
import tweepy
import time
from dotenv import load_dotenv
load_dotenv(override=True)

# import commands
from commands.ping import Ping
from commands.asterix import Asterix

# Auth on twitter and verify
auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))

api = tweepy.API(auth, wait_on_rate_limit=True)
try:
  api.verify_credentials()
  print("Auth is ok.")
except Exception as e:
  print("Can't Auth.")
  raise e

# Create the main loop listening for mentions
class MainListener():
  def __init__(self, api):
    self.api = api
    self.keywords = ["ping"]
    self.last_id = self.get_last_id()

    # get the different avaiable commands
    self.ping = Ping(api)
    self.asterix = Asterix(api)


  def check_mentions(self):
    new_id = 0
    mentions = tweepy.Cursor(self.api.mentions_timeline, since_id = self.last_id).items()

    for tweet in mentions:
      new_id = max(tweet.id, new_id)
      print(f"Mention from : {tweet.user.name}")

      # Checking if user asked for a ping
      if any(keyword in tweet.text.lower() for keyword in self.ping.keywords):
        self.ping.answer_tweet(tweet)

      elif any(keyword in tweet.text.lower() for keyword in self.asterix.keywords):
        if tweet.in_reply_to_status_id is not None:
          self.asterix.answer_tweet(tweet)      

    if new_id > self.last_id:
      self.set_last_id(new_id)


  def get_last_id(self):
    with open("assets/last_id.txt") as f:
      last_id = int(f.read().strip())
    return last_id

  def set_last_id(self, id):
    self.last_id = id
    with open("assets/last_id.txt", "w") as f:
      f.write(str(id))
    print(f"Last id is now {id}")


listener = MainListener(api)

while True:
  listener.check_mentions()
  print("Waiting")
  time.sleep(10)
    