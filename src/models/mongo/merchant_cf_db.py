from src.models.mongo.base import Base
from configs.configs import CONFIG_ACCOUNT_DB
from src.common.time import timestamp_utc
from src.common.constants import Rule


class MGconfig(Base):
    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB["MGConfig"]

    def update_custom(self, query, payload, updater = None, time = None):
        timer = time if time else timestamp_utc()
        if updater:
            payload['$set'].update({
                "update_by": updater,
                "update_at": timer
            })
            return self.col.update_one(query, payload)


    


