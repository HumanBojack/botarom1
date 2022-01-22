from PIL import Image, ImageFont, ImageDraw
import textwrap
import tweepy

class Asterix():
  def __init__(self, api):
    self.api = api
    self.keywords = ["asterix", "astérix", "pas compris", "pakompri"]


  def answer_tweet(self, tweet):
    print(f"Asterix to : {tweet.user.name}")
    try:
      original_tweet = self.api.get_status(tweet.in_reply_to_status_id, tweet_mode="extended")
    except:
      print(f"Can't fetch original tweet")
      return

    self.create_image(original_tweet.full_text)
    self.post_tweet(tweet.id)


  def create_image(self, text):
    image = Image.open("assets/asterix.png")
    draw = ImageDraw.Draw(image)

    if len(text) > 140:
      font_size = 35
      line_break = 25
    else:
      font_size = 50
      line_break = 17

    font = ImageFont.truetype("assets/Comic.ttf", font_size)
    lines = textwrap.wrap(text, width=line_break)

    t_width, t_height = font.getsize(text)
    y_text = (500 - t_height * len(lines)) / 2

    for line in lines:
      line_width, line_height = font.getsize(line)
      draw.text((360 - line_width / 2, y_text), line, font=font, fill=(0, 0, 0))
      y_text += 40
    
    image.save("assets/tweet_asterix.png")


  def post_tweet(self, tweet):
    try:
      image = self.api.media_upload("assets/tweet_asterix.png")

      self.api.update_status(
        status="",
        in_reply_to_status_id=tweet,
        auto_populate_reply_metadata=True,
        media_ids=[image.media_id]
      )
    except:
      print("Cant post tweet")