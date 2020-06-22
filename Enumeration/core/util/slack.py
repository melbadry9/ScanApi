import time
import requests
import logging 


slack_logger = logging.getLogger("core.utils.slack")
slack_logger.addHandler(logging.NullHandler())

def push_slack(hook:str, temp:list, domain:str):
    retry = 0
    done = False
    data = {
        "attachments": [
            {
                "color": "#f2c744", 
                "blocks": temp
                }
            ]
        }
    headers = {"Content-type": "application/json"}

    while not done:
        try:
            requests.post(hook, headers=headers, json=data)
            done = True
        
        # Avoid failure during posting to slack 
        except Exception:
            retry += 1
            slack_logger.error("{} - Posting to slack faild: Network error".format(domain))
            # Stop Retrying 
            if retry > 10:
                done = True

            # Sleep to avoid rate limit if it's the error
            time.sleep(2)

    slack_logger.debug("{} - Update posted to slack".format(domain))