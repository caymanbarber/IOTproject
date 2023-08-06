from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import json
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('deviceRegistration', __name__)



@login_required
@bp.route('/devices')
def deviceRegistration():
    
    

    return render_template('deviceRegistration/devReg.html')

@app.route('/api/add_<string:type>', methods=['POST'])
def add_item(type):
    match(type):
        case "device":
            print("get device request")
        case "sensor":
            print("get sensor request")
        case _:
            print("get request not matching")
            return jsonify({'message': 'Error'})
    data = request.json
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/api/add_sensor', methods=['POST'])
def add_item():
    data = request.json
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/api/delete_device/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    return jsonify({'message': 'Item not found'})

@app.route('/api/delete_device/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    return jsonify({'message': 'Item not found'})

@app.route('/api/get_sensor', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]
    return jsonify({'items': item_list})

