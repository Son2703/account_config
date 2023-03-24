

from configs.configs import CONFIG_ACCOUNT_DB
from src.common.common import CommonKey
from src.common.time import timestamp_utc
from src.models.mongo.base import Base
from configs.configs import USER_COL_NAME


class MGUser(Base):

    def __init__(self, col=None) -> None:
        Base.__init__(self, USER_COL_NAME)


    def update_without_updater(self, query, payload, updater=None):
        payload.update({
            CommonKey.UPDATE_AT: timestamp_utc()
        })
        try:
            self.col.update_one(query, {"$set": payload})
            return dict(payload)
        except Exception as error:
            raise error
        
