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
while loop < 10000:
    """check command from server
            """
    central_server_command_url = 'http://iot.namnguyenhoai.com:8000/api/central-server-command'
    query = {
        'device_ip': '127.0.0.1'
    }
    response = requests.get(central_server_command_url, params=query)
    data = response.json()
    if data['rollback'] is True:
        print('Start revert')
        timeout_in_second = 1
        cmd = 'git reset --hard'
        revert_start_time = time.time()
        result = subprocess.run(
            ['git', 'reset', '--hard', 'HEAD^1'], stdout=subprocess.PIPE, cwd='/home/namnguyen/django/rollback-client')
        revert_end_time = time.time()
        print(result.stdout)
        revert_execute_time = revert_end_time - revert_start_time
        print('Revert time: ' + str(revert_execute_time))
        revert_log_request = requests.post(log_url, {
            'type': 'git revert',
            'detail': result.stdout,
            'time_execution': revert_execute_time
        })
        print(revert_log_request.text)
        # pull new code
        print('Start pull')
        pull_start_time = time.time()
        result = subprocess.run(['git', 'pull', 'origin', 'device1'],
                                stdout=subprocess.PIPE, cwd='/home/namnguyen/django/rollback-client')
        pull_end_time = time.time()
        pull_execution_time = pull_end_time - pull_start_time
        print('Pull time: ' + str(pull_execution_time))
        pull_log_request = requests.post(log_url, {
            'type': 'git pull',
            'detail': result.stdout,
            'time_execution': pull_execution_time
        })
        print(pull_log_request.text)
        loop += 1
        print('Test No. ' + str(loop))
    else:
        print('No need to rollback')
    time.sleep(3)
