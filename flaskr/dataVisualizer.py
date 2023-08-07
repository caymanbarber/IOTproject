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
def index()->render_template:
    """Index of site - Data visualizer
    
    Serve page with data for chart
    Return: render_template
    """

    # Get user and DB
    user = g.user['username']
    db = get_db()

    # Retrieve data from DB for initial data visualizer page
    try:
        # Get list of sensors tied to user
        sensor_ids = get_sensor_list(db, user)
        dict = {}
        # Add data for each sensor to a dict
        for sensor in sensor_ids:
            # DB query to get data associated with user and sensor
            data = db.execute(
                ' SELECT username, sensor_id, sampled_time, sensor_value '
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}" AND sensor_id={sensor}'
                ' ORDER BY sampled_time ASC; '
            ).fetchall()
            
            # Format data
            data_array = []
            for row in data:
                data_array.append({"x":row[2],"y":row[3]})
            
            dict[sensor] = data_array

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
    """Handle api requests
    
    Adds post data to database and retrieves data for visualization 
    """
    
    if request.method == 'POST':
        return rest_data_post()
    
    if request.method == 'GET':
        date_range = {}
        # Parse data from get request
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

        # Parse list of device IDs to display
        if device_ids:
            try:
                if (type(device_ids[0]) == str):
                    device_ids = [int(numeric_string) for numeric_string in device_ids]
                if not(len(device_ids) >= 1 and type(device_ids[0]) == int):
                    raise ValueError("device_ids set incorrectly")
            except Exception as e:
                print(e)
                device_ids = []

        # Parse list of sensor IDs to display
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
    
def rest_data_get(date_range:dict, sensor_ids:list, device_ids:list)->dict:
    """Get request
    
    Keyword arguments:
    date-range -- dict of high and low dates to return values between
    sensor_ids -- list of sensor IDs to return values of
    device_ids -- list of device IDs to return values of
    Return: dict with data points, device_id list, and sensor_id list
    """
    
    # Get user and DB
    user = g.user['username']
    db = get_db()

    try:
        # Parse dates for searching of SQLite database
        date_low = str(datetime.fromisoformat(date_range["low"]).strftime('%Y-%m-%d %H:%M:%S'))
        date_high = str(datetime.fromisoformat(date_range["high"]).strftime('%Y-%m-%d %H:%M:%S'))
        data_dict = {}
    
        for key in sensor_ids:
            # Get query and parameters for database query
            (query, params) = construct_dynamic_query(device_ids,key,date_low,date_high)
            # Query database 
            data = db.execute(query,params).fetchall()
            
            # Parse query output
            data_array = []
            for row in data:
                data_array.append({"x":row[2],"y":row[3]})
            
            data_dict[key] = data_array
        
        return {"data": data_dict, 
                "device_list":get_device_list(db, user), 
                "sensor_list":get_sensor_list(db, user)}
    
    except Exception as e:
        print(e)
        return {"error":"e"}

        
def rest_data_post():
    """Post request
    """
    
    # Dict of labels and their intended type
    complete_keys = { "device_id": int, "sampled_time": str, "sensor_id": int, "sensor_value": float}

    # Get keys from data
    try:
        data = request.json
        data_keys = data.keys()
    except Exception as e:
        print(e)
        raise e

    error = None

    # Check if has all required keys
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
        print(error)
        response = {'message': error}
        return jsonify(response), 400

    else:
        db = get_db()
        # Insert data from request into database
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
    """get sensor list
    
    Keyword arguments:
    db -- database object
    user -- user object
    Return: list of sensor_ids
    """
    
    data = db.execute(
                ' SELECT DISTINCT username, sensor_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY sensor_id DESC; '
            ).fetchall()
    
    return list(set([row[1] for row in data]))

def get_device_list(db, user)->list:
    """get device list
    
    Keyword arguments:
    db -- database object
    user -- user object
    Return: list of device_ids
    """

    data = db.execute(
                ' SELECT DISTINCT username, device_id'
                ' FROM Iotdata i JOIN User u ON i.author_id = u.id '
                f' WHERE username="{user}"'
                ' ORDER BY device_id DESC; '
            ).fetchall()
    
    return list(set([row[1] for row in data]))

def construct_dynamic_query(device_ids:list=None, sensor_ids:list=None, date_low:list=None, date_high:list=None)->tuple:
    """Construct query with arguments
    
    Keyword arguments:
    device_ids -- List of device ids to query
    sensor_ids -- List of sensor ids to query
    date_low -- Bouding low date
    date_high -- Bounding high date
    Return: Tuple of Query and 
    """
    
    # Initialize the SQL query with the basic SELECT statement
    # 1=1 is added so that we can continue with AND
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

    return (query, params)