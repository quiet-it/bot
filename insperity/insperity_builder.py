import time
from hosts import *

class Insperity_builder:
    """Constructs different type of messages"""

    REPLY_BLOCK = {
        "type" : "section",
        "text" : {
            "type" : "mrkdwn",
            "text" : {}
        },
    }



    def __init__(self, user_id, channel, name='username'):
        self.channel = channel
        self.user_id = user_id
        self.timestamp = time.time()
        self.name = name

    def sites():


    def get_welcome(self):
        REPLY_BLOCK['text']['text'] = 'Welcome to IT-bot channel, ' + self.user_id
        return {
            "ts" : self.timestamp,
            "channel" : self.channel,
            "blocks" : [
                self.REPLY_BLOCK
            ]
        }

    def get_reply(self, text, name):
        self.REPLY_BLOCK['text']['text'] =  name + ' said: ' + text

        return {
            "ts" : self.timestamp,
            "channel" : self.channel,
            "blocks" : [
                self.REPLY_BLOCK
            ]
        }
