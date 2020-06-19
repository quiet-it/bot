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
slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
last_user = ''
onboarding_tutorials_sent = {}

def init_message(username, channel):
    b = Builder(username, channel)
    message = b.get_welcome()
    response = slack_web_client.chat_postMessage(**message)

@slack_events_adapter.on("message")
def menu():
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")


    if text and text.lower() == "menu":
            with open('result.json', 'a') as fp:
                json.dump(payload, fp)
                json.dump(',', fp)
        return init_message(user_id, channel_id)

@slack_events_adapter.on("team_join")
def onboarding_message(payload):
    event = payload.get("event", {})
    user_id = event.get('user')
    name = slack_web_client.users_info(user=user_id)
    channel = event.get('channel')
    init_message(user_id, channel, name)

# TODO: filter bot messages so it-bot wouldn't repeat them infinitly.
@slack_events_adapter.on("message")
def any_message(payload):
    event = payload.get("event", {})
    username = event.get('user')
    channel = event.get('channel')
    text = event.get("text")
    name = slack_web_client.users_info(user=username)
    print(name)
    b = Builder(username, channel)
    message = b.get_reply(text, name['user']['real_name'])
    # if 'bot_id' not in event and 'name' in event['user'] != 'itbot':
    if 'name' in event['user'] != 'itbot':
        response = slack_web_client.chat_postMessage(**message)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(debug=True)
    app.run(host="localhost", port=5000)
