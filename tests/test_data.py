import pytest
from flask import g, session
from flaskr.db import get_db
import json
from flaskr import dataPopulator

def test_index(client, auth):
    # Test index page
    response = client.get('/')
    assert response.status_code == 302

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data

def test_post(client, auth, app):
    # Test API post functinality 
    auth.login()
    response = client.post('/api/data', 
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"device_id": 2, 
                                            "sampled_time": '2018-01-01 00:00:00', 
                                            "sensor_id": 1, 
                                            "sensor_value": 0.001}))
    # Test good response
    assert response.json == {'message': 'Data received successfully'}
    assert response.status_code ==  200

    # Test db from previous post
    with app.app_context():
        db = get_db()
        dataPoint = db.execute('SELECT * FROM Iotdata WHERE id = 2').fetchone()
        assert dataPoint['device_id'] == 2
        assert dataPoint['sampled_time'] == '2018-01-01 00:00:00'
        assert dataPoint['sensor_id'] == 1
        assert dataPoint['sensor_value'] == 0.001

    # Test invalid API posts
    response = client.post('/api/data', 
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"device_id": 1, 
                                            "sampled_time": '2018-01-01 00:00:00', 
                                            "sensor_id": 1, 
                                            }))
    assert 'Request is invalid. Keys recieved:' in json.dumps(response.json)
    assert response.status_code ==  400

    response = client.post('/api/data', 
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"device_id": 1, 
                                            "sampled_time": '2018-01-01 00:00:00', 
                                            "sensor_id": 1, 
                                            "sensor_value": "0.001"
                                            }))
    assert 'Request is invalid. Value is of invalid type.' in json.dumps(response.json)
    assert response.status_code ==  400

def test_get(client, auth, app):
    # Test valid API get
    auth.login()
    response = client.get('/api/data?data_range_low=2023-07-10%2021:35:36'
                          '&data_range_high=2023-07-10%2023:15:36'
                          '&device_ids=1,2'
                          '&sensor_ids=1,2')
                        
    assert response.status_code ==  200
    print(response.json)