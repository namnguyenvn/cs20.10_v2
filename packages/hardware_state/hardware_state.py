from re import template
import time
import datetime


def state():
    current_time = datetime.datetime.now()

    with open(r"/sys/class/thermal/thermal_zone0/temp") as file:
        current_temp = file.readline()

    print(str(current_time) + " - " + str(float(current_temp) / 1000))
