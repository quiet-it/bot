from __future__ import print_function

import paramiko
import sys,os,time
from .hosts import *

def connect(site,clock='',command="/usr/bin/service"):
    print('CLOCK---', site, clock, command)
    # if clock == '':
    print('THIS IS SSH---------------')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.get_host_keys()
    client.connect(hosts[site][clock]['host'], username='root', password=hosts[site][clock]['pass'])
    stdin, stdout, stderr = client.exec_command(command)
    # print(str(stdout.read(),encoding='ascii'))
    time.sleep(50)
    print('THIS IS GET TRANSPORT---',client.get_transport())
    client.close()
    print('THIS IS GET TRANSPORT---',client.get_transport())
    # if client.get_transport() is not None:
    # return str(stdout.read(),encoding='ascii')
