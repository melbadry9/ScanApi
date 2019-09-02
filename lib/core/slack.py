import time
import json
import logging
import requests


slack_logger = logging.getLogger("slack")
slack_logger.addHandler(logging.NullHandler())

def push_slack(hook, string):
    retry = 0
    done = False
    data = {"text": string}
    headers = {"Content-type": "application/json"}

    while not done:
        try:
            res = requests.post(hook, headers=headers, json=data)
            status = str(res.status_code)
            done = True
        
        # Avoid failure during posting to slack 
        except Exception:
            retry += 1
            slack_logger.error("Posting to slack faild reason: ", exc_info=True)    
            # Stop Retrying 
            if retry > 10:
                status = "500"
                done = True
            # Sleep to avoid rate limit
            time.sleep(5)

    slack_logger.debug("Slack response code {0}".format(status))
