import os
from .hosts import *
from .ssh import *

class Insperity_commands:



    def __init__(self, clock):
        # self.hosts = hosts
        self.clock = clock

    def restart(self):
        for item in hosts:
            for item_2 in hosts[item]:
                if item_2 == self.clock:
                    print('RESTART')
                    response = connect(item, self.clock, 'restart')
        return response
