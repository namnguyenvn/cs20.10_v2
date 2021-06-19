import re
from re import template
import time
import datetime
import configparser
import os
import requests
import subprocess
import hashlib

print('Start checking rollback command')
loop = 0
log_url = 'http://iot.namnguyenhoai.com:8000/api/rollback-log'
#log_url = 'http://127.0.0.1:8000/api/rollback-log'
transaction_url = 'http://127.0.0.1:8000/api/transaction-search'
version_url = 'http://127.0.0.1:8000/api/package-version'
base_url = 'http://127.0.0.1:8000'
node_base_url = 'http://iot.namnguyenhoai.com:8000'
# copy version 2 to update
subprocess.run(['cp', 'dist/pi_temp-0.0.2.tar.gz',
               '/tmp/pi_temp-0.0.2.tar.gz'], cwd='/home/namnguyen/django/cs20.10_v2/packages')
# seed the node
seed_response = requests.post(
    node_base_url + '/api/seed', data={'node_address': '127.0.0.1'})
# print(seed_response.json())

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
        # register node
        register_response = requests.post(
            base_url + '/api/nodes/register', data={'nodes[]': 'http://127.0.0.1:5000'})
        print(register_response.json())
        rollback_start_time = time.time()
        # sync data from another node
        # sync chain
        print('sync chain')
        sync_response = requests.get(base_url + '/api/nodes/resolve')
        print(sync_response.json())
        # search transaction
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
        print(download_url)
        # download_request = requests.get(download_url, allow_redirects=True)
        filename = ''
        if download_url.find('/'):
            filename = '/tmp/' + download_url.rsplit('/', 1)[1]
        subprocess.run(['wget', download_url, '-O', filename])
        # open(filename, 'wb').write(download_request.content)
        # check sum
        md5_downloaded_file = hashlib.md5(
            open(filename, 'rb').read()).hexdigest()
        if md5_downloaded_file == version['file_hash']:
            print('Same MD5')
            # install file
            print('Start install pip')
            pip_install_result = subprocess.run(
                ['pip', 'install', filename], stdout=subprocess.PIPE)
            print(pip_install_result.stdout)
            rollback_end_time = time.time()
            execution_time = rollback_end_time - rollback_start_time
            pull_log_request = requests.post(log_url, {
                'type': '(dev) blockchain sync rollback',
                'detail': pip_install_result.stdout,
                'time_execution': execution_time
            })
            print(pull_log_request.text)
        else:
            print('Not same MD5')
            print(md5_downloaded_file)
            print(version['file_hash'])
        loop += 1
        print('Test No. ' + str(loop))
        # empty chain
        empty_chain_response = requests.post(base_url + '/api/empty-chain')
        print(empty_chain_response.json())
        # install back the higher version
        print('Start install pip')
        pip_install_result = subprocess.run(
            ['pip', 'install', '/tmp/pi_temp-0.0.2.tar.gz'], stdout=subprocess.PIPE)
        print(pip_install_result.stdout)
    else:
        print('No need to rollback')
    time.sleep(1)
