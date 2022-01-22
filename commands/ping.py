import tweepy
class Ping():
  def __init__(self, api):
    self.api = api
    self.keywords = ["ping"]

  def answer_tweet(self, tweet):
    print(f"Pong to : {tweet.user.name}")

    try:
      self.api.update_status(
        status="pong",
        in_reply_to_status_id=tweet.id,
        auto_populate_reply_metadata=True
      )
    except:
      print("Cant post tweet")