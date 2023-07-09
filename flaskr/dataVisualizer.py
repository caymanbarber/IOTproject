from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('data', __name__)


@bp.route('/')
@login_required
def index():
    
    
    return render_template('data/data.html')


@bp.route('/api', methods=['POST'])
@login_required
def restEndpoint():
    complete_keys = { "device_id": int, "sampled_time": str, "sensor_id": int, "sensor_value": float}

    if request.method == 'POST':
        data = request.json
        data_keys = data.keys()

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


    