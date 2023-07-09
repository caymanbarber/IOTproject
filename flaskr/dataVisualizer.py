from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from json import JSONDecoder, JSONEncoder
bp = Blueprint('data', __name__)

@bp.route('/')
def index():
    
    
    return render_template('data/data.html')

@bp.route('/api', methods=['POST'])
def restEndpoint():
    data = JSONDecoder(request.json)
    data_keys = data.keys()

    complete_keys = ["device_id", "sampled_time", "sensor_id", "sensor_value"]




    response = {'message': 'Data received successfully'}
    return JSONEncoder(response), 200
    