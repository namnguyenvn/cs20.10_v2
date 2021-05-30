from re import template
import time
import datetime
import configparser
import os
import requests

print('Start checking rollback command')
while(True):
    """check command from server
            """
    central_server_command_url = 'http://iot.namnguyenhoai.com:8000/api/central-server-command'
    query = {
        'device_ip': '127.0.0.1'
    }
    response = requests.get(central_server_command_url, params=query)
    data = response.json()
    if data['rollback'] is True:
        print('Needs to rollback')
    else:
        print('No need to rollback')
    time.sleep(3)
