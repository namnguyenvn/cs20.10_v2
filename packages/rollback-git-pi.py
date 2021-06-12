from re import template
import time
import datetime
import configparser
import os
import requests
import subprocess

print('Start checking rollback command')
loop = 0
log_url = 'http://iot.namnguyenhoai.com:8000/api/rollback-log'
pi_git_path = '/home/pi/rollback-client'
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
        revert_result = subprocess.run(
            ['git', 'reset', '--hard', 'HEAD^1'], stdout=subprocess.PIPE, cwd=pi_git_path)
        revert_end_time = time.time()
        print(revert_result.stdout)
        print('Start install pip')
        pip_install_result = subprocess.run(
            ['pip', 'install', 'pi_temp.tar.gz'], stdout=subprocess.PIPE, cwd=pi_git_path)
        print(pip_install_result.stdout)
        revert_execute_time = revert_end_time - revert_start_time
        print('Revert time: ' + str(revert_execute_time))
        revert_log_request = requests.post(log_url, {
            'type': 'git revert',
            'detail': revert_result.stdout + pip_install_result.stdout,
            'time_execution': revert_execute_time
        })
        print(revert_log_request.text)
        # pull new code
        print('Start pull')
        pull_start_time = time.time()
        pull_result = subprocess.run(['git', 'pull', 'origin', 'device1'],
                                     stdout=subprocess.PIPE, cwd=pi_git_path)
        print('Start install pip')
        pip_install_result = subprocess.run(
            ['pip', 'install', 'pi_temp.tar.gz'], stdout=subprocess.PIPE, cwd=pi_git_path)
        print(pip_install_result.stdout)
        pull_end_time = time.time()
        pull_execution_time = pull_end_time - pull_start_time
        print('Pull time: ' + str(pull_execution_time))
        pull_log_request = requests.post(log_url, {
            'type': 'git pull',
            'detail': pull_result.stdout + pip_install_result.stdout,
            'time_execution': pull_execution_time
        })
        print(pull_log_request.text)
        loop += 1
        print('Test No. ' + str(loop))
    else:
        print('No need to rollback')
    time.sleep(1)
