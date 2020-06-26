import os
import logging
from flask import Flask, request, json
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from builder import Builder
import  requests
from urllib.parse import parse_qs
from werkzeug.datastructures import ImmutableMultiDict
from insperity import Insperity_commands
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
    # print(type(request.form))
    # # print('THIS IS FORM--------',json.loads(request.form))
    imd = ImmutableMultiDict(request.form)
    data = imd.to_dict()
    # requests.post(data['response_url'],'200')
    # print('THIS IS DATA +++++++++++', data)
    # # data = json.loads(request.form["payload"])
    # channel_id = data['channel_id']
    ins = Insperity(payload)
    # print('THIS IS SITES================',ins.sites())
    # slack_web_client.chat_postMessage(
    #     channel=channel_id,
    #     blocks = ins.sites()
    #     )
    print( data)
    return {
        "blocks" : ins.sites(),
        "response_type": "in_channel",

    }

@app.route('/receive', methods=['POST'])
def receive(payload='no payload'):
    # data = json.loads(request.form["payload"])
    imd = ImmutableMultiDict(request.form)
    data = imd.to_dict()
    data = json.loads(data['payload'])
    print("THIS IS DATA---------------", data)
    channel_id = data['container']['channel_id']
    user = data['user']['name']
    value = data['actions'][0]['value']
    site = data['actions'][0]['text']['text'].split()
    site = site[0].lower()
    resp = {}

    ins = Insperity(data)
    # if 'actions' in data:
    # print('THIS IS VALUE=======', value)
    # print('THIS IS ACTIONS======', data['actions'][0]['value'], ' = ', tmp_arr)
    if data['actions'][0]['text']['text'] == 'Reboot':
        print('THIS IS SSH+++++++++++++++++++')
        ssh = Insperity_commands(value)
        ssh.restart()
        resp = {
            "text" : 'Restart in progress',
            # "blocks" : ins.custom_button('Reboot',value),
            "response_type": "in_channel"
        }
        requests.post(data['response_url'],json=resp)
    if value in ins.host_name():
        # print('IF PASSED======================')
        resp = {
            "blocks" : ins.custom_button('Reboot',value),
            "response_type": "in_channel"
        }
        requests.post(data['response_url'],json=resp)

    else:
        # print('ELSE PASSED======================')
        resp =  {
            # "channel" : channel_id,
            "blocks" : ins.site_clocks(data['actions'][0]['value']),
            "response_type": "in_channel"
        }
        # requests.post('https://slack.com/api/chat.postMessage',json=resp)
        requests.post(data['response_url'],json=resp)
    return ''

    # tmp_arr = ins.host_name(value)
        # return json.jsonify(resp)
        # slack_web_client.chat_postMessage(
        #     channel=channel_id,
        #     blocks = ins.site_clocks(data['actions'][0]['value'])
        #     )
        # event = ins.site_clocks(data['actions'][0]['value'])
        #
        # slack_web_client.chat_postMessage(
        #     channel=channel_id,
        #     blocks = event['blocks']
        #     )
        # print("THIS IS FORM -------------",request.form['payload'])
        # print(type(request.form['payload']))
        # dic = json.loads(request.form['payload'])
    # print("THIS IS DIC----------->",dic['container']['channel_id'])
    # for elem in dic:
    #     print(dic[elem])
    # print("THIS IS FORM ELEMENT -------------",type(json.loads(request.form['payload'])))
    # print("THIS IS FORM ELEMENT SECOND-------------",json.loads(request.form['payload']['type']))
    # print('THIS IS FORM-----------',ins.form)
    # response_url = data['response_url']
    # requests.post(response_url, json=event, headers=headers)
    # post = requests.post(data['response_url'], json=response, headers=headers)
    # print(post)
    # response = slack_web_client.chat_postMessage(event)
    # return event

# @slack_events_adapter.on("")
# def menu():w
#     event = payload.get("event", {})
#
#     channel_id = event.get("channel")
#     user_id = event.get("user")
#     text = event.get("text")
#
#     b = Builder(username, channel)
#
#     if text and text.lower() == "menu":
#             with open('result.json', 'a') as fp:
#                 json.dump(payload, fp)
#                 json.dump(',', fp)
#             return init_message(user_id, channel_id)

# @slack_events_adapter.on("team_join")
# def onboarding_message(payload):
#     event = payload.get("event", {})
#     user_id = event.get('user')
#     name = slack_web_client.users_info(user=user_id)
#     channel = event.get('channel')
#     init_message(user_id, channel, name)
#
# # TODO: filter bot messages so it-bot wouldn't repeat them infinitly.
# @slack_events_adapter.on("message")
# def any_message(payload):
#     event = payload.get("event", {})
#     username = event.get('user')
#     channel = event.get('channel')
#     text = event.get("text")
#     name = slack_web_client.users_info(user=username)
#     print(name)
#     b = Builder(username, channel)
#     message = b.get_reply(text, name['user']['real_name'])
#     # if 'bot_id' not in event and 'name' in event['user'] != 'itbot':
#     if 'name' in event['user'] != 'itbot':
#         response = slack_web_client.chat_postMessage(**message)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(debug=True)
    app.run(host="localhost", port=5000)
