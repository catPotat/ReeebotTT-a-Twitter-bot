import tweepy
import logging
from dotenv import load_dotenv
load_dotenv()
import os
import time
import datetime
from bot_functions import palette_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


API_KEY = os.getenv('TWITTER_BOT_KEY')
API_SECRET_KEY = os.getenv('TWITTER_BOT_SECRET_KEY')

ACCESS_TOKEN = os.getenv('rbgtx_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('rbgtx_ACCESS_TOKEN_SECRET')


def main():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except:
        raise Exception("Authentication not OK")

    since_id = 1
    with open('data/since_id.txt', 'a'): pass
    with open('data/since_id.txt', 'r+') as f:
        content = f.read()
        if content.isnumeric():
            since_id = int(content)
    while True:
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
            since_id = max(tweet.id, since_id)
            palette_maker.make_palette(tweet, api)
        
        with open('data/since_id.txt', 'w') as f:
            f.write(str(since_id))
        now = datetime.datetime.now()
        if now.minute % 60 == 0:
            logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    main()
