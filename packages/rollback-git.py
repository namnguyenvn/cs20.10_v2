from re import template
import time
import datetime
import configparser
import os
import requests
import subprocess

print('Start checking rollback command')
loop = True
#log_url = 'http://iot.namnguyenhoai.com:8000/api/rollback-log'
log_url = 'http://127.0.0.1:8000/api/rollback-log'
while(loop):
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
        timout_in_second = 1
        cmd = 'git reset --hard'
        start_time = time.time()
        result = subprocess.run(
            ['git', 'reset', '--hard', 'HEAD^1'], stdout=subprocess.PIPE, cwd='/home/namnguyen/django/rollback-client')
        end_time = time.time()
        print(result.stdout)
        execute_time = end_time - start_time
        print('Execute time: ' + str(execute_time))
        log_request = requests.post(log_url, {
            'device': 1,
            'detail': 'device 1',
            'time_execution': execute_time
        })
        print(log_request.text)
        loop = False
    else:
        print('No need to rollback')
    time.sleep(3)
