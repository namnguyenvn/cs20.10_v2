from re import template
import time
import datetime
import configparser
import os


def state():
    path_current_directory = os.path.dirname(__file__)
    path_config_file = os.path.join(
        path_current_directory, 'configuration', 'config.ini')
    config = configparser.ConfigParser()
    config.read(path_config_file)

    print(config.get("server", "central_server_address"))
    print(config.get("device", "device_name"))
    gateway_items = config.items("gateways")
    for gateway, gateway_address in gateway_items:
        print(gateway + ': ' + gateway_address)

    while(True):
        current_time = datetime.datetime.now()

        with open(r"/sys/class/thermal/thermal_zone0/temp") as file:
            current_temp = file.readline()

        print(str(current_time) + " - " + str(float(current_temp) / 1000))

        time.sleep(5)
