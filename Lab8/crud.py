import uuid
import requests
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ElectroScooter(Base):
    __tablename__ = 'electro_scooters'

    id = Column(String, primary_key=True)
    name = Column(String)
    battery_level = Column(Integer)

class CRUDElectroScooter:
    def __init__(self, leader: bool, followers: dict = None, db_url: str = None):
        self.leader = leader
        self.followers = followers
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_electro_scooter(self, data):
        if self.leader:
            scooter_id = str(uuid.uuid4())
            data['id'] = scooter_id

            electro_scooter = ElectroScooter(**data)

            with self.Session() as session:
                session.add(electro_scooter)
                session.commit()

            for follower in self.followers:
                requests.post(
                    f"http://{follower['host']}:{follower['port']}/electro-scooter",
                    json=data,
                    headers={"Token": "Leader"}
                )

            return data, 201
        else:
            return {"error": "Cannot create Electro Scooter. This instance is not the leader."}, 403

    def get_electro_scooter(self, scooter_id):
        with self.Session() as session:
            scooter = session.query(ElectroScooter).get(scooter_id)
            if scooter:
                return {
                    "id": scooter.id,
                    "name": scooter.name,
                    "battery_level": scooter.battery_level
                }, 200
            else:
                return {"error": "Electro Scooter not found"}, 404

    def get_all_electro_scooters(self):
        with self.Session() as session:
            scooters = session.query(ElectroScooter).all()

        if scooters:
            scooter_list = []
            for scooter in scooters:
                scooter_details = {
                    "id": scooter.id,
                    "name": scooter.name,
                    "battery_level": scooter.battery_level
                }
                scooter_list.append(scooter_details)
            return scooter_list, 200
        else:
            return {"error": "No Electro Scooters found in the database"}, 404

    def update_electro_scooter(self, scooter_id, data):
        with self.Session() as session:
            scooter = session.query(ElectroScooter).get(scooter_id)
            if scooter:
                for key, value in data.items():
                    setattr(scooter, key, value)

                if self.leader:
                    for follower in self.followers:
                        requests.put(
                            f"http://{follower['host']}:{follower['port']}/electro-scooter/{scooter_id}",
                            json=data,
                            headers={"Token": "Leader"}
                        )

                session.commit()
                return data, 200
            else:
                return {"error": "Electro Scooter not found"}, 404

    def delete_electro_scooter(self, scooter_id):
        with self.Session() as session:
            scooter = session.query(ElectroScooter).get(scooter_id)
            if scooter:
                deleted_scooter = {
                    "id": scooter.id,
                    "name": scooter.name,
                    "battery_level": scooter.battery_level
                }
                session.delete(scooter)

                if self.leader:
                    for follower in self.followers:
                        requests.delete(
                            f"http://{follower['host']}:{follower['port']}/electro-scooter/{scooter_id}",
                            headers={"Token": "Leader"}
                        )

                session.commit()
                return deleted_scooter, 200
            else:
                return {"error": "Electro Scooter not found"}, 404
