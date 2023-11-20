from flask import Flask, request
from crud import CRUDElectroScooter

service_info = {
    "host": "127.0.0.1",
    "port": 5000,
    "leader": True
}

followers = [
    {
        "host": "127.0.0.1",
        "port": 5001
    },
    {
        "host": "127.0.0.1",
        "port": 5002
    }
]

crud_electro_scooter = CRUDElectroScooter(service_info["leader"], followers, db_url="postgresql://postgres:password1234@localhost:5432/postgres")

app = Flask(__name__)


@app.route("/api/electro-scooters", methods=["POST"])
def create_electro_scooter():
    headers = dict(request.headers)
    if not crud_electro_scooter.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "message": "Access denied!"
        }, 403
    else:
        return_dict, status_code = crud_electro_scooter.create_electro_scooter(request.json)
        return return_dict, status_code


@app.route("/api/electro-scooters/<string:scooter_id>", methods=["GET"])
def get_electro_scooter_by_id(scooter_id):
    return_dict, status_code = crud_electro_scooter.get_electro_scooter(scooter_id)
    return return_dict, status_code


@app.route("/api/electro-scooters", methods=["GET"])
def get_all_electro_scooters():
    return_dict, status_code = crud_electro_scooter.get_all_electro_scooters()
    return return_dict, status_code


@app.route("/api/electro-scooters/<string:scooter_id>", methods=["PUT"])
def update_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud_electro_scooter.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "message": "Access denied!"
        }, 403
    else:
        new_data = request.json
        return_dict, status_code = crud_electro_scooter.update_electro_scooter(scooter_id, new_data)
        return return_dict, status_code


@app.route("/api/electro-scooters/<string:scooter_id>", methods=["DELETE"])
def delete_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud_electro_scooter.leader and ("Token" not in headers or headers["Token"] != "Leader"):
        return {
            "message": "Access denied!"
        }, 403
    else:
        return_dict, status_code = crud_electro_scooter.delete_electro_scooter(scooter_id)
        return return_dict, status_code


if __name__ == '__main__':
    app.run(
        host=service_info["host"],
        port=service_info["port"]
    )
