import time

class Builder:
    """Constructs different type of messages"""

    REPLY_BLOCK = {
        "type" : "section",
        "text" : {
            "type" : "mrkdwn",
            "text" : {}
        },
    }



    def __init__(self, username, channel):
        self.channel = channel
        self.username = username
        self.timestamp = time.time()

    def get_welcome(self):
        REPLY_BLOCK['text']['text'] = 'Welcome to IT-bot channel, ' + self.username
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
