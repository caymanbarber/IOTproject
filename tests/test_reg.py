import sqlite3

import pytest
import json
from flask import g, session
from flaskr.db import get_db

def test_device_reg(client, auth):
    auth.login()
    response = client.get('/devices')
    assert response.status_code == 200
    # TODO: Add more after page development

def test_get_reg_items(client, auth, app):
    auth.login()
    # Test device get
    response = client.get('/devices/api/get_device')
    assert response.status_code ==  200
    print(response.json)

    # Test sensor get

    response = client.get('/devices/api/get_sensor')
    assert response.status_code == 200
    print(response.json)

    # Test incorrect inputs
    # TODO

def test_update_reg_item(client, auth, app):
    auth.login()

    # Test updating device 
    response = client.put('/devices/api/update_device/1',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 1, 
                                            "device_name": 'New device 1', 
                                            "details": 'Here are new details', 
                                            "city": 'Los Angeles',
                                            "coordinates": "23.84453,11.18660"})
                           )
    assert response.status_code ==  200
    print(response.json)

    # Test updating sensor
    response = client.put('/devices/api/update_sensor/1',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 1, 
                                            "sensor_name": 'New sensor 1', 
                                            "unit": 'F'})
                           )
    assert response.status_code == 200
    print(response.json)

    with app.app_context():
        db = get_db()
        dataPoint = db.execute('SELECT * FROM Devices WHERE id = 1').fetchone()
        print([dataPoint[thing] for thing in dataPoint.keys()])
        assert dataPoint['device_name'] == 'New device 1'
        assert dataPoint['details'] == 'Here are new details'
        assert dataPoint['city'] == 'Los Angeles'
        assert dataPoint['coordinates'] == '23.84453,11.18660'

        dataPoint = db.execute('SELECT * FROM Sensors WHERE id = 1').fetchone()
        assert dataPoint['sensor_name'] == 'New sensor 1'
        assert dataPoint['unit'] == 'F'

    # Test incorrect inputs
    # TODO

def test_generate_id(client, auth, app):
    # Test generating id 
    auth.login()
    response = client.get('/devices/api/generate_device_id')
    print(response.json)
    assert response.json['id'] != 1
    assert response.status_code == 200

    response = client.get('/devices/api/generate_sensor_id')
    print(response.json)
    assert response.json['id'] != 1
    assert response.status_code == 200

    # Test incorrect inputs
    # TODO

def test_delete_reg_item(client, auth, app):
    
    # Add device to DB
    auth.login()
    response = client.post('/devices/api/add_device',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 2, 
                                            "device_name": 'New device 2', 
                                            "details": 'Here are new details', 
                                            "city": 'Los Angeles',
                                            "coordinates": "23.84453,11.18660"})
                           )
    # Add sensor to DB
    response = client.post('/devices/api/add_sensor',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 2, 
                                            "sensor_name": 'New sensor 2', 
                                            "unit": 'F'})
                           )
    
    # Test deleting device 
    response = client.delete('/devices/api/delete_device/2')
    assert response.json == {'message': 'Item deleted successfully'}
    assert response.status_code ==  200

   # Test deleting sensor
    response = client.delete('/devices/api/delete_sensor/2')

    assert response.json == {'message': 'Item deleted successfully'}
    assert response.status_code ==  200

    with app.app_context():
        db = get_db()
        dataPoint = db.execute('SELECT * FROM Devices WHERE id = 2').fetchone()
        assert dataPoint is None

        dataPoint = db.execute('SELECT * FROM Sensors WHERE id = 2').fetchone()
        assert dataPoint is None

    # Test incorrect inputs
    # TODO

def test_add_reg_item(client, auth, app):
    # Test appending device 
    
    auth.login()
    response = client.post('/devices/api/add_device',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 2, 
                                            "device_name": 'New device 2', 
                                            "details": 'Here are new details', 
                                            "city": 'Los Angeles',
                                            "coordinates": "23.84453,11.18660"})
                           )
    
    assert response.json == {'message': 'Item added successfully'}
    assert response.status_code ==  200
    
    # Test appending sensor

    response = client.post('/devices/api/add_sensor',
                           headers={'Content-Type': 'application/json'}, 
                           data=json.dumps({"id": 2, 
                                            "sensor_name": 'New sensor 2', 
                                            "unit": 'F'})
                           )
    
    assert response.json == {'message': 'Item added successfully'}
    assert response.status_code ==  200

    with app.app_context():
        db = get_db()
        dataPoint = db.execute('SELECT * FROM Devices WHERE id = 2').fetchone()
        assert dataPoint['device_name'] == 'New device 2'
        assert dataPoint['details'] == 'Here are new details'
        assert dataPoint['city'] == 'Los Angeles'
        assert dataPoint['coordinates'] == '23.84453,11.18660'

        dataPoint = db.execute('SELECT * FROM Sensors WHERE id = 2').fetchone()
        assert dataPoint['sensor_name'] == 'New sensor 2'
        assert dataPoint['unit'] == 'F'

    # Test incorrect inputs
    # TODO
