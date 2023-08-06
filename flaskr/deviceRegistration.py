from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import json
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('deviceRegistration', __name__)


# put is update?

@bp.route('/devices')
@login_required
def deviceRegistration():
    
    

    return render_template('deviceRegistration/devReg.html')

class Object:
    def __init__(self):
        pass

    def __init__(self, id:int):
        self.id = id

class Sensor(Object):
    def __init__(self):
        pass

    def __init__(self, id:int, sensorName:str = None, unit:str = None) -> None:
        super(Sensor,self).__init__(id)
        self.sensorName = sensorName
        self.unit = unit

    def add():
        pass

    def update():
        pass

    def delete():
        #check item is in db first
        pass

    def get():
        pass

class Device(Object):
    def __init__(self):
        pass

    def __init__(self, id:int, deviceName:str = None, details:str = None, 
                 city:str = None, coordinates:str = None) -> None:
        super(Sensor,self).__init__(id)
        self.deviceName = deviceName
        self.details = details
        self.city = city
        self.coordinates = coordinates

@bp.route('/devices/api/add_<string:type>', methods=['POST'])
@login_required
def add_reg_item(type):
    data = request.json
    match(type):
        case "device":
            object = Device(id=data['id'], deviceName=data['device_name'], details=data['details'],
                            city=data['city'], coordinates=data['coordinates'])
            print("get device request")
        case "sensor":
            object = Sensor(id=data['id'],sensorName=data['sensor_name'],unit=data['unit'])
            print("get sensor request")
        case _:
            print("get request not matching")
            return jsonify({'message': 'Error'})
    
    object.add()

    return jsonify({'message': 'Item added successfully'})

@bp.route('/devices/api/delete_<string:type>/<int:item_id>', methods=['DELETE'])
@login_required
def delete_reg_item(type, item_id):
    match(type):
        case "device":
            object = Device(id=item_id)
            print("delete device request")
        case "sensor":
            object = Sensor(id=item_id)
            print("delete sensor request")
        case _:
            print("delete request not matching")
            return jsonify({'message': 'Error'})
    object.delete()
    return jsonify({'message': 'Item deleted successfully'})


@bp.route('/devices/api/get_<string:type>', methods=['GET'])
@login_required
def get_reg_items(type):
    match(type):
        case "device":
            object = Device()
            print("get device request")
        case "sensor":
            object = Sensor()
            print("get sensor request")
        case _:
            print("get request not matching")
            return jsonify({'message': 'Error'})

    #TODO
    item_list = object.get()
    return jsonify({'items': item_list})

@bp.route('/devices/api/update_<string:type>', methods=['PUT'])
@login_required
def update_reg_items(type):
    data = request.json
    match(type):
        case "device":
            object = Device(id=data['id'], deviceName=data['device_name'], details=data['details'],
                            city=data['city'], coordinates=data['coordinates'])
            print("put device request")
        case "sensor":
            object = Sensor(id=data['id'],sensorName=data['sensor_name'],unit=data['unit'])
            print("put sensor request")
        case _:
            print("put request not matching")
            return jsonify({'message': 'Error'})

    return jsonify({'message': 'Item updated successfully'})
    

