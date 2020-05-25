import requests
import json
import os 


HEADERS = {
    'Content-type': 'application/json'
}


def slacker():
    # I have saved my slack webhook in an environment variable called SLACK_WEBHOOK
    webhook_url = os.environ.get("SLACK_WEBHOOK")
    def slack_it(msg):
        payload = {'text': msg}
        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slack_it
