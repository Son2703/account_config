from datetime import datetime
from src.common.common import CommonKey

class Base:
    def __init__(self, col = None) -> None:
        self.col = col

    def filter_one(self, payload):
        return self.col.find(payload)
    
    def filter_all(self, payload):
        return [x for x in self.col.find(payload)]

    def update_one(self, query, payload, updater = None):
        if updater:
            payload.update({
                CommonKey.UPDATE_BY: updater,
                CommonKey.UPDATE_AT: datetime.now()
            })
            return self.col.update_one(query, payload)

    def create(self, payload, creator = None):
        if creator:
            payload.update({
                CommonKey.CREATE_BY: creator,
                CommonKey.UPDATE_BY: None,
                CommonKey.CREATE_AT: None,
                CommonKey.UPDATE_AT: datetime.now()
            })
        return self.col.insert_one(payload)
    
    def delete_all(self):
        return self.col.delete_many({})
