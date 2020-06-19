import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
client.
try:
  response = client.chat_postMessage(
    channel="C0XXXXXX",
    text="Hello from your app! :tada:"
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

print(client.rtm_read())
