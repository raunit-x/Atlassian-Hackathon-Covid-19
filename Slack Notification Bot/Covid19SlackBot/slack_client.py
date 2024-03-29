import requests
import json
import os 


HEADERS = {
    'Content-type': 'application/json'
}


def slacker():
    webhook_url = os.environ.get("SLACK_WEBHOOK")
    def slack_it(msg):
        payload = {'text': msg}
        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slack_it
