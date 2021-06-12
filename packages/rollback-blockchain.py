import re
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
version_url = 'http://127.0.0.1:8000/api/package-version'
base_url = 'http://127.0.0.1:8000/'
while loop < 1000:
    """check command from server
            """
    central_server_command_url = 'http://iot.namnguyenhoai.com:8000/api/central-server-command'
    query = {
        'device_ip': '127.0.0.1'
    }
    rollback_start_time = time.time()
    response = requests.get(central_server_command_url, params=query)
    data = response.json()
    if data['rollback'] is True:
        print('start rollback')
        print('get info from blockchain')
        transaction_query = {
            'device': 'Device 1',
            'version': '0.0.1'
        }
        response = requests.get(transaction_url, params=transaction_query)
        transaction = response.json()
        print('Transaction')
        print(transaction)
        # find in server the file to download
        version_query = {
            'device': 'Device 1',
            'version': '0.0.1',
            'file_hash': transaction['file_hash']
        }
        print(version_url)
        response = requests.get(version_url, version_query)
        json_response = response.json()
        version = json_response['version']
        print('version_result')
        print(version)
        # download file
        download_url = base_url + version['file']
        download_request = requests.get(download_url, allow_redirects=True)
        filename = 'file-versions' + \
            version['device'] + '-' + version['version']
        open(filename, 'wb').write(download_request.content)
    else:
        print('No need to rollback')
    time.sleep(3)
