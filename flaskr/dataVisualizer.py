from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import json
from datetime import datetime
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
        keys = get_sensor_list(db, user)
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


@bp.route('/api/data', methods=['POST','GET'])
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
        date_range = {}
        date_low = request.args["data_range_low"]
        date_high = request.args["data_range_high"]
        device_ids = request.args.getlist("device_ids")[0].split(',')
        sensor_ids = request.args.getlist("sensor_ids")[0].split(',')

        if date_low:
            date_range["low"] = date_low
            
        if date_high:
            date_range["high"] = date_high

        if not date_range:
            date_range = {}

        if device_ids:
            try:
                if (type(device_ids[0]) == str):
                    device_ids = [int(numeric_string) for numeric_string in device_ids]
                if not(len(device_ids) >= 1 and type(device_ids[0]) == int):
                    raise ValueError("device_ids set incorrectly")
            except Exception as e:
                print(e)
                device_ids = []

        if sensor_ids:
            try:
                if (type(sensor_ids[0]) == str):
                    sensor_ids = [int(numeric_string) for numeric_string in sensor_ids]
                if not(len(sensor_ids) >= 1 and type(sensor_ids[0]) == int):
                    raise ValueError("sensor_ids set incorrectly")
            except Exception as e:
                print(e)
                sensor_ids = []       

        return rest_data_get(date_range, sensor_ids, device_ids)
    
def rest_data_get(date_range, sensor_ids, device_ids):
    user = g.user['username']

    db = get_db()
    try:
        #sensor_id
        #keys = [1, 2]

        print(datetime.fromisoformat(date_range["low"]))
        print(datetime.fromisoformat(date_range["low"]).strftime('%Y-%m-%d %H:%M:%S'))

        date_low = str(datetime.fromisoformat(date_range["low"]).strftime('%Y-%m-%d %H:%M:%S'))
        date_high = str(datetime.fromisoformat(date_range["high"]).strftime('%Y-%m-%d %H:%M:%S'))
        data_dict = {}
        print(sensor_ids)
        print(type(sensor_ids))
        for key in sensor_ids:

            (query, params) = construct_dynamic_query(device_ids,key,date_low,date_high)
            
            data = db.execute(query,params).fetchall()


            #TODO: Add device_ids and date_range
            
            data_array = []
            for row in data:
                data_array.append({"x":row[2],"y":row[3]})
            
            print(str(data_array))
            data_dict[key] = data_array

        print(str(data_dict))
        print ("done")
        
        return {"data": data_dict, 
                "device_list":get_device_list(db, user), 
                "sensor_list":get_sensor_list(db, user)}
    
    except Exception as e:
        print(e)
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
                ' SELECT DISTINCT username, sensor_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY sensor_id DESC; '
            ).fetchall()
    #data[rows][user sensor_id]
    return list(set([row[1] for row in data]))

def get_device_list(db, user):
    data = db.execute(
                ' SELECT DISTINCT username, device_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY device_id DESC; '
            ).fetchall()
    #data[rows][user sensor_id]
    return list(set([row[1] for row in data]))

def construct_dynamic_query(device_ids=None, sensor_ids=None, date_low=None, date_high=None):
    # Initialize the SQL query with the basic SELECT statement

    query = "SELECT username, sensor_id, sampled_time, sensor_value FROM Iotdata i JOIN User u ON i.author_id = u.id WHERE 1=1"

    # Add conditions based on user input
    params = []

    if device_ids:
        if isinstance(device_ids, list):
            if len(device_ids) == 1:
                query += " AND device_id = ?"
                params.append(device_ids[0])
            else:
                placeholders = ','.join(['?' for _ in device_ids])
                query += f" AND device_id IN ({placeholders})"
                params.extend(device_ids)
        else:
            query += " AND device_id = ?"
            params.append(device_ids)

    if sensor_ids:
        if isinstance(sensor_ids, list):
            if len(sensor_ids) == 1:
                query += " AND sensor_id = ?"
                params.append(sensor_ids[0])
            else:
                placeholders = ','.join(['?' for _ in sensor_ids])
                query += f" AND sensor_id IN ({placeholders})"
                params.extend(sensor_ids)
        else:
            query += " AND sensor_id = ?"
            params.append(sensor_ids)

    if date_low and date_high:
        query += " AND sampled_time BETWEEN ? AND ?"
        params.extend([date_low, date_high])

    query += " ORDER BY sampled_time ASC;"

    print(query)
    print(params)
    return query, params