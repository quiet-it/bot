import os
import logging
from flask import Flask, request, json
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from builder import Builder
import  requests
from urllib.parse import parse_qs
from werkzeug.datastructures import ImmutableMultiDict
from insperity.commands import Insperity_commands
import ssl as ssl_lib
import certifi
from insperity.insperity import Insperity

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
# print(os.environ['SLACK_SIGNING_SECRET'])
app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)
# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
channel_id = ''
tmp_arr = []
onboarding_tutorials_sent = {}

def init_message(username, channel):
    b = Builder(username, channel)
    message = b.get_welcome()
    response = slack_web_client.chat_postMessage(**message)

@app.route('/insperity', methods=['POST'])
def insperity(payload=''):
    imd = ImmutableMultiDict(request.form)
    data = imd.to_dict()
    ins = Insperity(payload)
    return {
        "blocks" : ins.sites(),
        "response_type": "in_channel",

    }

@app.route('/receive', methods=['POST'])
def receive(payload='no payload'):
    imd = ImmutableMultiDict(request.form)
    data = imd.to_dict()
    data = json.loads(data['payload'])
    channel_id = data['container']['channel_id']
    user = data['user']['name']
    value = data['actions'][0]['value']
    site = data['actions'][0]['text']['text'].split()
    site = site[0].lower()
    resp = {}

    ins = Insperity(data)
    if data['actions'][0]['text']['text'] == 'Reboot':
        ssh = Insperity_commands(value)
        answer = ssh.restart()
        resp = {
            "text" : 'Restart may take a several minutes',
            "response_type": "in_channel"
        }
        print('THIS IS DATA--==========',data)
        requests.post(data['response_url'],json=resp)

    if value in ins.host_name(): #
        resp = {
            "blocks" : ins.custom_button('Reboot',value),
            "response_type": "in_channel"
        }
        requests.post(data['response_url'],json=resp)
    else:
        resp =  {
            "blocks" : ins.site_clocks(data['actions'][0]['value']),
            "response_type": "in_channel"
        }
        requests.post(data['response_url'],json=resp)
    return ''



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(debug=True)
    app.run(host="localhost", port=5000)
