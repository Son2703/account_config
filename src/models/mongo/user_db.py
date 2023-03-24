

from configs.configs import CONFIG_ACCOUNT_DB
from src.common.common import CommonKey
from src.common.constants import DatabaseName
from src.common.time import timestamp_utc
from src.models.mongo.base import Base
from src.common.constants import DatabaseName


class MGUser(Base):

    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB[DatabaseName.COL_USER.value]


    def update_without_updater(self, query, payload, updater=None):
        payload.update({
            CommonKey.UPDATE_AT: timestamp_utc()
        })
        try:
            self.col.update_one(query, {"$set": payload})
            return dict(payload)
        except Exception as error:
            raise error
        
