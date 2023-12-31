"""Post API script for testing

Make post API requests as a peripheral IoT device would
"""

import json
import requests
from datetime import datetime, timedelta
import csv
from math import sin, cos
from random import random
import sys

uri = 'http://127.0.0.1:5000'

login = {
    'username': 'cayman',
    'password': '?%M9ZCmSJ#sG5)f'
}

debug = False

def start_session():
    with requests.Session() as s:
        print("logging in ... ")
        p = s.post(uri+'/auth/login', data=login)
        if debug:
            print(p)
        date = datetime.strptime("2023-07-10 21:35:36", '%Y-%m-%d %H:%M:%S')
        
        for i in range(100):
            date = generate_date(date,timedelta(minutes=1))
            data = generate_data(1, print_date(date), 3, sin(i) + 1 + random())
            p = post_data(s, data)
            if debug:
                print(data)
                print(p)

def post_data(s, data):
    p = s.post(uri+'/api/data', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    return p

def generate_data(device_id, sampled_time, sensor_id, sensor_value):
    data = {"device_id": device_id, 
            "sampled_time": sampled_time, 
            "sensor_id": sensor_id, 
            "sensor_value": sensor_value}
    return data

def generate_date(last_date=None, delta_time=timedelta(minutes=1)):

    if last_date == None:
        date = datetime.now()
    else:
        date = last_date + delta_time

    return date

def print_date(date):
    return str(date.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    if '--debug' in sys.argv:
        debug = True
    start_session()