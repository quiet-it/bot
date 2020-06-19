import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from builder import Builder
import json
import ssl as ssl_lib
import certifi

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SECRET, "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=TOKEN)
last_user = ''
onboarding_tutorials_sent = {}

def init_message(username, channel):
    b = Builder(username, channel)

    message = b.get_welcome()

    response = slack_web_client.chat_postMessage(**message)

@slack_events_adapter.on("team_join")
def onboarding_message(payload):
    event = payload.get("event", {})

    username = event.get('user')

    channel = event.get('channel')

    init_message(username, channel)

@slack_events_adapter.on("message")
def onboarding_message(payload):


    event = payload.get("event", {})
    username = last_user = event.get('user')
    channel = event.get('channel')
    text = event.get("text")
    name = slack_web_client.users_info(username)
    print(name)
    b = Builder(username, channel)
    message = b.get_reply(text, name['profile']['real_name'])
    if 'bot_id' not in event :
        response = slack_web_client.chat_postMessage(**message)
    # last_user = username
    # with open('result.json', 'a') as fp:
    #     json.dump(payload, fp)
    #     json.dump(',', fp)
    # return response

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(debug=True)
    app.run(port=3000)
