from abc import ABC, abstractmethod
import re


class NeutronSource(ABC):

    # req_fields = ["name" "angular_params", "angular_function", "energetic_function",]

    def __init__(
        self,
        client,
    ) -> None:
        self.client = client

    def _required_fields_checker(self, data):
        for i in data.keys():
            if data[i] is None or len(data[i]) == 0:
                raise ValueError(
                    f"<{i}> field is required to continue"
                )
        return data
    

class Cyclotrone(NeutronSource):
    # COLLECTION = "cyclotrone"
    COLLECTION = "Cyclotrone"
    def __init__(self, client):
        super().__init__(client)
        self.collection = self.client.Cyclotrone


    def get_all_names(self):
        
        res = self.collection.find({"source_type": "cyclotrone"})

        return [
            v for i in res 
            for k, v in i.items() 
            if k == "name"
        ]

    def get_source(self, name):
        res = self.collection.find_one({"name": name})
        del res["_id"]  #* removes ObjectId
        return res

    def insert(self, data: dict):
        self._required_fields_checker(data)
        self.collection.insert_one(data)
        
        return f"source <{data.get('name')}> inserted"

    def update(self, name: str, data: dict):
        query = {"name": name}
        res = self.collection.update_one(query, data)
        
        if res.raw_result.get("updatedExisting"):
            if res.raw_result.get("nModified"):
                return f"source <{name}> has been updated"
            return f"nothing to update in source <{name}>"
        
        return f"source <{name}> not found"

    def delete(self, name: str):
        query = {"name": name}
        res = self.collection.delete_one(query)
    
        if res.raw_result.get("n"):
            return f"source <{name}> has been deleted"
        return f"there is no source <{name}> to delete"


    def fetch(self, query):
        res = self.collection.find(query)
        return res

class ThermalReactor(NeutronSource):
    def __init__(self):
        return