

from configs.configs import CONFIG_ACCOUNT_DB
from src.models.mongo.base import Base


class MGUser(Base):

    def __init__(self, col=None) -> None:
        super().__init__(col)
        # common format, need follow
        self.col = CONFIG_ACCOUNT_DB["users"]


    def update_without_updater(self, query, payload, updater=None):
        try:
            self.col.update_one(query, {"$set": payload})
            return dict(payload)
        except Exception as error:
            raise error
        
    def find_extra(self, payload):
        rs = self.col.find(**payload)
        return list(rs)