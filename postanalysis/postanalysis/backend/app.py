from flask import Flask, request, jsonify
from crontab import CronTab
import tweepy
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def schedule_tweet(text, datetime_str):
    cron = CronTab(user=True)
    # Parse the datetime string to a datetime object
    tweet_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    # Create a cron expression for the given datetime
    cron_expression = f"{tweet_time.minute} {tweet_time.hour} {tweet_time.day} {tweet_time.month} *"
    command = f'/usr/bin/python3 /mnt/c/Users/DELL/Downloads/postanalysis/postanalysis/backend/tweet.py "{text}" > /tmp/cron_log.txt 2>&1'


    job = cron.new(command=command, comment='scheduled_tweet')
    job.setall(cron_expression)
    cron.write()

def schedule_facebook_post(text, time):
    cron = CronTab(user=True)
    post_time = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    cron_expression = f"{post_time.minute} {post_time.hour} {post_time.day} {post_time.month} *"
    command = f'/usr/bin/python3 /mnt/c/Users/DELL/Downloads/postanalysis/postanalysis/backend/facebook.py "{text}" > /tmp/cron_log.txt 2>&1'
    job = cron.new(command=command, comment='scheduled_facebook_post')
    job.setall(cron_expression)
    cron.write()

# Endpoint to schedule a tweet
@app.route('/schedule_tweet', methods=['POST'])
def schedule_tweet_endpoint():
    try:
        data = request.get_json()
        schedule_tweet(data['text'], data['time'])
        return jsonify({"message": "Tweet scheduled successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/create_facebook_post', methods=['POST'])
def create_facebook_post():
    try:
        data = request.get_json()
        schedule_facebook_post(data['text'], data['time'])
        return jsonify({"message": "Facebook post scheduled successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=7000, debug=True)
