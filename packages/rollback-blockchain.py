from re import template
import time
import datetime
import configparser
import os
import requests
import subprocess

print('Start checking rollback command')
loop = 0
#log_url = 'http://iot.namnguyenhoai.com:8000/api/rollback-log'
log_url = 'http://127.0.0.1:8000/api/rollback-log'
transaction_url = 'http://127.0.0.1:8000/api/transaction-search'
while loop < 1000:
    """check command from server
            """
    central_server_command_url = 'http://iot.namnguyenhoai.com:8000/api/central-server-command'
    query = {
        'device_ip': '127.0.0.1'
    }
    response = requests.get(central_server_command_url, params=query)
    data = response.json()
    if data['rollback'] is True:
        print('start rollback')
        print('get info from blockchain')
        query = {
            'device': 'Device 1',
            'version': '0.0.1'
        }
        response = requests.get(transaction_url, params=query)
        transaction = response.json()
        print(transaction)
    else:
        print('No need to rollback')
    time.sleep(3)
