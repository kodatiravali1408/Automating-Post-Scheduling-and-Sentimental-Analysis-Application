import tweepy
import sys
import os
from dotenv import load_dotenv
load_dotenv()
from crontab import CronTab

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with Twitter using Tweepy
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def send_tweet(message):
    client.create_tweet(text=message)
    print("Tweeted!")

def remove_cron_jobs(comment):
    cron = CronTab(user=True)
    jobs_to_remove = [job for job in cron if job.comment == comment]
    for job in jobs_to_remove:
        cron.remove(job)
    cron.write()

if __name__ == "__main__":
    tweet_text = sys.argv[1] if len(sys.argv) > 1 else "Hello World!"
    send_tweet(tweet_text)
    remove_cron_jobs('scheduled_tweet')
