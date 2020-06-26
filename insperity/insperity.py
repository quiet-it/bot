from .templates import *
from .hosts import *
import json, copy

class Insperity:

    def __init__(self, data):
        if type(data) is not str:
            self.data = data
            self.event = self.data.get("event",{})
            self.user_id = self.event.get("user")
            self.text = self.event.get('text')
            self.value = data['actions'][0]['value']
            # self.temp = sites
            # self.hosts = self.host_name(self.value)
            # self.sites = self.sites()

    def sites(self): #Return site buttons
        body = copy.deepcopy(block_body) #
        button = copy.deepcopy(block_button)
        for host in hosts:
            button['text']['text'] = host.capitalize()
            button['value'] = host
            c = copy.deepcopy(button)
            body['blocks'][1]['elements'].append(c)
        return body['blocks']

    def site_clocks(self, site): #Returns
        body = copy.deepcopy(block_body) #
        button = copy.deepcopy(block_button)
        for host in hosts[site]:
            button['text']['text'] = hosts[site][host]["description"]
            button['value'] = host
            c = copy.deepcopy(button)
            body['blocks'][1]['elements'].append(c)
            body
        return body['blocks']

    def custom_button(self, text, value):
        body = copy.deepcopy(block_body) #
        button = copy.deepcopy(block_button)
        button['text']['text'] = text
        button['value'] = value
        body['blocks'][1]['elements'].append(button)
        # for host in hosts:
        #     c = copy.deepcopy(button)
        return body['blocks']

    def host_name(self):
        tmp = []
        for site in hosts:
            for host in hosts[site]:
                tmp.append(host)
        return tmp
