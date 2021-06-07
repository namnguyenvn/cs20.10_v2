""" version 0.0.2 """
from re import template
import time
import datetime
import configparser
import os
import requests

from sense_emu import SenseHat

sense = SenseHat()


def temp():
    """ Get temp and post to server
    """
    path_current_directory = os.path.dirname(__file__)
    path_config_file = os.path.join(
        path_current_directory, 'configuration', 'config.ini')
    config = configparser.ConfigParser()
    config.read(path_config_file)

    print(config.get("server", "central_server_address"))
    print(config.get("device", "device_ip"))
    gateway_items = config.items("gateways")
    for gateway, gateway_address in gateway_items:
        print(gateway + ': ' + gateway_address)

    while(True):
        """send data to central server
        """
        current_time = datetime.datetime.now()

        temp = sense.temp

        print(str(current_time) + " - " + str(temp))

        device_temp_url = 'http://' + config.get("server", "central_server_address") + \
            ':8000/api/device-temp'

        data = {
            'device_ip': config.get("device", "device_ip"),
            'temp': temp,
            'timestamp': current_time
        }

        x = requests.post(device_temp_url, data=data)

        print(x.status_code)

        time.sleep(3)
