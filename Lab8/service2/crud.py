import requests


class CrudElectroScooter:
    def __init__(self, leader: bool, followers: dict = None):
        self.leader = leader
        if self.leader:
            self.followers = followers

    def post_electro_scooter(self, user_dict: dict):
        if self.leader:
            for follower in self.followers:
                requests.post(f"http://{follower['host']}:{follower['port']}/api/electro-scooters",
                              json=user_dict,
                              headers={"Token": "Leader"})

    def update_electro_scooter(self, index: str, user_dict: dict):
        if self.leader:
            for follower in self.followers:
                requests.put(f"http://{follower['host']}:{follower['port']}/api/electro-scooters/{index}",
                             json=user_dict,
                             headers={"Token": "Leader"})

    def delete_electro_scooter(self, index: str):
        if self.leader:
            for follower in self.followers:
                requests.delete(f"http://{follower['host']}:{follower['port']}/api/electro-scooters/{index}",
                                headers={"Token": "Leader", "X-Delete-Password": "pr"})
