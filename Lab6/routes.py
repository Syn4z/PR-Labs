import json
from flask import request, jsonify
from models.database import db
from models.electro_scooter import ElectroScooter
from __main__ import app


@app.route('/api/electro-scooters', methods=['POST'])
def create_electro_scooter():
    try:
        data = request.get_json()
        name = data['name']
        battery_level = data['battery_level']
        electro_scooter = ElectroScooter(name=name, battery_level=battery_level)
        db.session.add(electro_scooter)
        db.session.commit()
        return jsonify({"message": "Electro Scooter created successfully"}), 201
    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['GET'])
def get_electro_scooter_by_id(scooter_id):
    scooter = ElectroScooter.query.get(scooter_id)
    if scooter is not None:
        return jsonify({
            "id": scooter.id,
            "name": scooter.name,
            "battery_level": scooter.battery_level
        }), 200
    else:
        return jsonify({"error": "Electro Scooter not found"}), 404


@app.route('/api/electro-scooters', methods=['GET'])
def get_all_electro_scooters():
    scooters = ElectroScooter.query.all()

    if scooters:
        scooter_list = []
        for scooter in scooters:
            scooter_details = {
                "id": scooter.id,
                "name": scooter.name,
                "battery_level": scooter.battery_level
            }
            scooter_list.append(scooter_details)
        return jsonify(scooter_list), 200
    else:
        return jsonify({"error": "No Electro Scooters found in the database"}), 404


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
def update_electro_scooter(scooter_id):
    try:
        scooter = ElectroScooter.query.get(scooter_id)
        if scooter is not None:
            data = request.get_json()
            scooter.name = data.get('name', scooter.name)
            scooter.battery_level = data.get('battery_level', scooter.battery_level)
            db.session.commit()
            return jsonify({"message": "Electro Scooter updated successfully"}), 200
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
def delete_electro_scooter(scooter_id):
    try:
        scooter = ElectroScooter.query.get(scooter_id)
        if scooter is not None:
            # Get the password from the request headers
            password = request.headers.get('X-Delete-Password')
            if password == 'pr':
                db.session.delete(scooter)
                db.session.commit()
                return jsonify({"message": "Electro Scooter deleted successfully"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
