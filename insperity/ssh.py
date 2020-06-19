from __future__ import print_function

import paramiko
import sys,os

def connect(site,clock='',command="/usr/bin/service"):
    if clock == '':
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.get_host_keys()
        client.connect(hosts[site][clock]['host'], username='root', password=hosts[site][clock]['pass'])
        stdin, stdout, stderr = client.exec_command(command)
        print(str(stdout.read(),encoding='ascii'))
        client.close()
