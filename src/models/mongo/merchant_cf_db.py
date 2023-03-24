from src.models.mongo.base import Base
from configs.configs import CONFIG_ACCOUNT_DB
from src.common.time import timestamp_utc
from src.common.constants import DatabaseName
from src.common.common import CommonKey


class MGMerchantRuleAssignment(Base):
    def __init__(self, col=None) -> None:
        super().__init__(col)
        self.col = CONFIG_ACCOUNT_DB[DatabaseName.COL_MERCHANT_RULE_ASSIGNMENT.value]

    def update_custom(self, query, payload, updater = None, time = None):
        timer = time if time else timestamp_utc()
        if updater:
            payload.update({
                "update_by": updater,
                "update_at": timer
            })
            return self.col.update_one(query, {"$set": payload})
        
    def create_many_config(self, payload, creator=None):
        time_create = timestamp_utc()
        data_update = {
                CommonKey.CREATE_BY: creator,
                CommonKey.UPDATE_BY: None,
                CommonKey.CREATE_AT: time_create,
                CommonKey.UPDATE_AT: None
            }
        for item in payload:
            item.update(data_update)
        self.col.insert_many(payload)
        return data_update


    


