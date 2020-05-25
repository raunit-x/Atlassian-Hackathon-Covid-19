import requests
import json
import os 


HEADERS = {
    'Content-type': 'application/json'
}


def slacker(webhook_url='https://hooks.slack.com/services/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'):
    def slack_it(msg):
        payload = {'text': msg}
        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slack_it
