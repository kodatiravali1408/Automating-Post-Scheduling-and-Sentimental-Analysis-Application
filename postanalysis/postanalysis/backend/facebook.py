import requests
import os
import sys
from crontab import CronTab
from dotenv import load_dotenv

load_dotenv()

def post_to_facebook(message):
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    page_id = os.getenv('FACEBOOK_PAGE_ID')  # Your Facebook Page ID
    url = f'https://graph.facebook.com/{page_id}/feed'

    payload = {
        'message': message,
        'access_token': access_token
    }

    response = requests.post(url, data=payload)
    return response.json()

def remove_cron_jobs(comment):
    cron = CronTab(user=True)
    jobs_to_remove = [job for job in cron if job.comment == comment]
    for job in jobs_to_remove:
        cron.remove(job)
    cron.write()

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Default message"
    result = post_to_facebook(message)
    print(result)
    remove_cron_jobs('scheduled_facebook_post')
