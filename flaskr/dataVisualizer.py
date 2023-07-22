from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import json
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('data', __name__)


@bp.route('/')
@login_required
def index():
    #get data
    
    user = g.user['username']

    db = get_db()
    try:
        #sensor_id
        keys = [1, 2]
        dict = {}
        for key in keys:
            data = db.execute(
                ' SELECT username, sensor_id, sampled_time, sensor_value '
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}" AND sensor_id={key}'
                ' ORDER BY sampled_time ASC; '
            ).fetchall()
            
            data_array = []
            for row in data:
                data_array.append({"x":row[2],"y":row[3]})
            
            dict[key] = data_array
        
        
        #flash(json.dumps(dict))
        return render_template('data/data.html', 
                               data=dict, 
                               device_list=get_device_list(db, user),
                               sensor_list=get_sensor_list(db, user) )
    except Exception as e:
        flash(e)

    return render_template('data/data.html', data="problem")


@bp.route('/api/data', methods=['POST'])
@login_required
def restEndpoint():

    if request.method == 'POST':
        return rest_data_post()
    
    if request.method == 'GET':
        """
        request.json

        from request.json get date_range
        from request.json get sensor_ids
        from request.json get device_ids

        """
        date_low = request.args["data_range_low"]
        date_high = request.args["data_range_high"]
        device_ids = request.args["device_ids"]
        sensor_ids = request.args["sensor_ids"]




        if date_low:
            date_range["low"] = date_low
            
        if date_high:
            date_range["high"] = date_high

        if not date_range:
            date_range = {}

        if device_ids:
            try:
                if not(len(device_ids) >= 1 and type(device_ids[0]) == int):
                    raise ValueError("device_ids set incorrectly")
            except Exception as e:
                flash(e)
                device_ids = []

        if sensor_ids:
            try:
                if not(len(device_ids) >= 1 and type(device_ids[0]) == int):
                    raise ValueError("device_ids set incorrectly")
            except Exception as e:
                flash(e)
                device_ids = []       

        return rest_data_get(date_range, sensor_ids, device_ids)
    
def rest_data_get(date_range, sensor_ids, device_ids):
    user = g.user['username']

    db = get_db()
    try:
        #sensor_id
        #keys = [1, 2]
        dict = {}
        for key in sensor_ids:
            data = db.execute(
                ' SELECT username, sensor_id, sampled_time, sensor_value '
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}" AND sensor_id={key}'
                ' ORDER BY sampled_time ASC; '
            ).fetchall()
            #TODO: Add device_ids and date_range
            
            data_array = []
            for row in data:
                data_array.append({"x":row[2],"y":row[3]})
            
            dict[key] = data_array
        
        return {"data": dict, 
                "device_list":get_device_list(db, user), 
                "sensor_list":get_sensor_list(db, user)}
    
    except Exception as e:
        flash(e)
        return {"error":"e"}

        
def rest_data_post():
    complete_keys = { "device_id": int, "sampled_time": str, "sensor_id": int, "sensor_value": float}

    try:
        data = request.json
        data_keys = data.keys()
    except Exception as e:
        print(e)
        raise e

    error = None
    
    if set(data_keys).intersection(set(complete_keys.keys())) != complete_keys.keys():
        error = 'Request is invalid. Keys recieved:'
        for key in data_keys:
            error += " " + str(key)
        error += ". Needs: "
        for key in complete_keys:
            error += " " + str(key)
    else:
        for key in complete_keys.keys():
            if type(data[key]) != complete_keys[key]:
                error = 'Request is invalid. Value is of invalid type. '
                error += key + ' type:' + type(data[key]).__name__ + ' =/= ' + complete_keys[key].__name__

    if error is not None:
        flash(error)
        response = {'message': error}
        return jsonify(response), 400

    else:
        db = get_db()
        try:
            db.execute(
                'INSERT INTO Iotdata (author_id, device_id, sampled_time, sensor_id, sensor_value)'
                ' VALUES (?, ?, ?, ?, ?)',
                (g.user['id'], data['device_id'], data['sampled_time'], data['sensor_id'], data['sensor_value'])
            )
        except ValueError:
            error = 'Value error. Cannot update DB'
            flash(error)
            response = {'message': error}
            return jsonify(response), 400
        db.commit()
        response = {'message': 'Data received successfully'}
        return jsonify(response), 200
    
def get_sensor_list(db, user):
    data = db.execute(
                ' SELECT username, sensor_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY sensor_id DESC; '
            ).fetchall()
    #data[rows][user sensor_id]
    return list(set([row[1] for row in data]))

def get_device_list(db, user):
    data = db.execute(
                ' SELECT username, device_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY device_id DESC; '
            ).fetchall()
    #data[rows][user sensor_id]
    return list(set([row[1] for row in data]))