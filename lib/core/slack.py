import json
import logging
import requests


slack_logger = logging.getLogger("slack")
slack_logger.addHandler(logging.NullHandler())

def push_slack(hook, string):
    data = {"text": string}
    headers = {"Content-type": "application/json"}
    try:
        res = requests.post(hook, headers=headers, json=data)
    except Exception:
        slack_logger.error("Slack ", exc_info=True)
    slack_logger.debug("Slack response code {0}".format(str(res.status_code)))
