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
            slack_logger.error("Posting to slack faild reason: ", exc_info=True)
            time.sleep(5)
            retry += 1

        # Stop Retrying 
        if not retry < 5:
            status = "500"
            done = True

    slack_logger.debug("Slack response code {0}".format(status))
