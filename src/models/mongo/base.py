from datetime import datetime
from src.common.common import CommonKey
from src.common.time import timestamp_utc

class Base:
    def __init__(self, col = None) -> None:
        self.col = col

    def filter_one(self, payload = None):
        return self.col.find_one(payload)
    
    def find(self, payload = None, skip = None, limit = None):
        rs = self.col.find(payload)
        if limit:
            rs = rs.limit(limit)
        if skip:
            rs  = rs.skip(skip)
        return [x for x in rs]

    def update_one(self, query, payload, updater = None):
        if updater:
            payload.update({
                CommonKey.UPDATE_BY: updater,
                CommonKey.UPDATE_AT: timestamp_utc()
            })
            return self.col.update_one(query, payload)

    def create(self, payload, creator = None):
        if creator:
            payload.update({
                CommonKey.CREATE_BY: creator,
                CommonKey.UPDATE_BY: None,
                CommonKey.CREATE_AT: None,
                CommonKey.UPDATE_AT: timestamp_utc()
            })
        return self.col.insert_one(payload)
    
    def create_many(self, payload, creator = None):
        pass
    
    def delete_all(self):
        return self.col.delete_many({})
