from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import json
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db
import random
bp = Blueprint('deviceRegistration', __name__)


# put is update?

@bp.route('/devices')
@login_required
def deviceRegistration():
    """Serve the device registration page
    """

    #TODO: Add default gets to populate page on init

    return render_template('deviceRegistration/devReg.html')

class Object:
    """Parent common object of Sensor and Device
    """
    id = None
    name = None
    user = None
    db = None
    table = None

    def __init__(self, table:str, id:int = None, name:str = None)->None:
        self.table = table
        self.id = id
        self.name = name
        self.user = g.user['username']
        self.db = get_db()

    def pullQuery(self, query, params):
        data = self.db.execute(query,params).fetchall()
        return self.process_data(data)
    
    def pushQuery(self, query, params):
        self.db.execute(query,params)
        self.db.commit()

    def get_all(self):
        query = f"SELECT * FROM {self.table}"
        params = []
        return self.pullQuery(query,params)
    
    def delete(self):
        if self.get_one({"id":self.id}) is None:
            raise RuntimeError("This entry does not exist")
        
        query = f"DELETE FROM {self.table} WHERE id = {self.id}"
        params = []

        self.pushQuery(query,params)
        

class Sensor(Object):
    def __init__(self, table:str, id:int = None , sensorName:str = None, unit:str = None) -> None:
        super(Sensor,self).__init__(table, id, sensorName)
        self.unit = unit

    def add(self):
        if self.name is None:
            raise RuntimeError("No name given")
        
        if len(self.get_one({"id":self.id})) > 0:
            raise RuntimeError("This entry already exists")
        
        query = f"INSERT INTO {self.table} (id, sensor_name, unit) VALUES (?, ?, ?)"
        params = (self.id, self.name, self.unit)
        self.pushQuery(query, params)

    def update(self):
        if self.get_one({"id":self.id}) is None:
            raise RuntimeError("This entry does not exist")
        
        if self.name is None:
            raise RuntimeError("No name given")
        query = f"UPDATE {self.table} SET (sensor_name, unit) = (?, ?) WHERE id = '{self.id}'"
        params = (self.name, self.unit)

        self.pushQuery(query,params)

    def get_one(self,input:dict):
        query = f"SELECT * FROM {self.table} WHERE 1=1"
        params = []

        if "id" in input.keys() and input["id"] is not None:
            query += " AND id = ?"
            params.append(input["id"])

        elif input["sensor_name"] is not None:
            query += " AND sensor_name = ?"
            params.append(input["sensor_name"])

        output = self.pullQuery(query,params)

        if output is not None and len(output) > 0:
            return output[0]
        
        return []
    
    def process_data(self, data):
        return [
            {"id": row[0], "sensor_name": row[1], "unit": row[2]} 
             for row in data
            ]

class Device(Object):
    def __init__(self, table:str, id:int = None, deviceName:str = None, details:str = None, 
                 city:str = None, coordinates:str = None) -> None:
        super(Device,self).__init__(table, id, deviceName)
        self.details = details
        self.city = city
        self.coordinates = coordinates

    def add(self):
        if self.name is None:
            raise RuntimeError("No name given")
        
        if len(self.get_one({"id":self.id})) > 0:
            raise RuntimeError("This entry already exists")
        
        query = f"INSERT INTO {self.table} (id, device_name, details, city, coordinates) VALUES (?, ?, ?, ?, ?)"
        params = (self.id, self.name, self.details, self.city, self.coordinates)
        self.pushQuery(query, params)

    def update(self):
        if self.get_one({"id":self.id}) is None:
            raise RuntimeError("This entry does not exist")

        if self.name is None:
            raise RuntimeError("No name given")
        print(self.name)
        query = f"UPDATE {self.table} SET (device_name, details, city, coordinates) = (?, ?, ?, ?) WHERE id = '{self.id}'"
        params = (self.name, self.details, self.city, self.coordinates)

        self.pushQuery(query,params, )

    def get_one(self,input:dict):
        query = f"SELECT * FROM {self.table} WHERE 1=1"
        params = []

        if "id" in input.keys() and input["id"] is not None:
            query += " AND id = ?"
            params.append(input["id"])

        elif input["device_name"] is not None:
            query += " AND sensor_name = ?"
            params.append(input["device_name"])

        output = self.pullQuery(query,params)

        if output is not None and len(output) > 0:
            return output[0]
        
        return []

    def process_data(self, data):
        return [
            {"id": row["id"], "device_name": row["device_name"], "details": row["details"],
             "city": row["city"], "coordinates": row["coordinates"]} 
             for row in data
            ]

@bp.route('/devices/api/add_<string:type>', methods=['POST'])
@login_required
def add_reg_item(type:str):
    """Add specified item to correct list
    
    Keyword arguments:
    type -- type of object to add: device, sensor
    Return: status message
    """

    data = request.json
    match(type):
        case "device":
            object = Device(table = "Devices", id=data['id'], deviceName=data['device_name'], details=data['details'],
                            city=data['city'], coordinates=data['coordinates'])
            print("get device request")
        case "sensor":
            object = Sensor(table = "Sensors", id=data['id'],sensorName=data['sensor_name'],unit=data['unit'])
            print("get sensor request")
        case _:
            print("get request not matching")
            return jsonify({'message': 'Error'})
    try:
        object.add()
    except Exception as e:
        print(e)
        return jsonify({'message': e})

    return jsonify({'message': 'Item added successfully'})

@bp.route('/devices/api/delete_<string:type>/<int:item_id>', methods=['DELETE'])
@login_required
def delete_reg_item(type, item_id):
    """Delete specified item to correct list
    
    Keyword arguments:
    type -- type of object to delete: device, sensor
    item_id -- id of item to delete
    Return: status message
    """

    match(type):
        case "device":
            object = Device(table = "Devices", id=item_id)
            print("delete device request")
        case "sensor":
            object = Sensor(table = "Sensors", id=item_id)
            print("delete sensor request")
        case _:
            print("delete request not matching")
            return jsonify({'message': 'Error'})
        
    try:
        object.delete()
    except Exception as e:
        print(e)
        return jsonify({'message': e})

    return jsonify({'message': 'Item deleted successfully'})

@bp.route('/devices/api/get_<string:type>', methods=['GET'])
@login_required
def get_reg_items(type):
    """Get all items to correct list
    
    Keyword arguments:
    type -- type of object to add: device, sensor
    Return: items matching query
    """

    match(type):
        case "device":
            object = Device(table = "Devices")
            print("get device request")
        case "sensor":
            object = Sensor(table = "Sensors")
            print("get sensor request")
        case _:
            print("get request not matching")
            return jsonify({'message': 'Error'})

    try:
        item_list = object.get_all()
        
    except Exception as e:
        print(e)
        return jsonify({'message': e,'items': []})

    return jsonify({'items': item_list})

@bp.route('/devices/api/update_<string:type>/<int:item_id>', methods=['PUT'])
@login_required
def update_reg_items(type, item_id):
    """update specified item to correct list
    
    Keyword arguments:
    type -- type of object to add: device, sensor
    Return: status message
    """
    #TODO: build out request args 
    data = request.json
    if data['id'] and item_id != data['id']:
        print("IDs not matching")
        return jsonify({'message': e})
    
    match(type):
        case "device":
            object = Device(table = "Devices", id=item_id, deviceName=data['device_name'], details=data['details'],
                            city=data['city'], coordinates=data['coordinates'])
            print("put device request")
        case "sensor":
            object = Sensor(table = "Sensors", id=item_id, sensorName=data['sensor_name'],unit=data['unit'])
            print("put sensor request")
        case _:
            print("put request not matching")
            return jsonify({'message': 'Error'})
        
    try:
        object.update()
    except Exception as e:
        print(e)
        return jsonify({'message': e})

    return jsonify({'message': 'Item updated successfully'})
    
@bp.route('/devices/api/generate_<string:type>_id', methods=['GET'])
@login_required
def generate_unique_id(type:str):
    """Create unique ID for specific type
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    match(type):
        case "device":
            object = Device(table = "Devices")
        case "sensor":
            object = Sensor(table = "Sensors")
        case _:
            return jsonify({'message': 'Error'})
    id = 1
    data = object.get_all()

    while id < 10000:
        if id not in [thing["id"] for thing in data]:
            return jsonify({'id':id})
        id += 1
    raise RuntimeError("No free IDs")
