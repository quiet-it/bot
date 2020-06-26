import os
from hosts import *
from ssh import *

class Insperity_commands:



    def __init__(self, clock):
        # self.hosts = hosts
        self.clock = clock

    def restart(self, clock):
        for item in hosts:
            for item_2 in item:
                if item_2 == clock:
                    connect(self.clock, 'restart')

        return print('Reboot in progress')
