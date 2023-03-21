from src.models.mongo.base import Base
from configs.configs import RULE_COL_NAME
from src.common.common import CommonKey
from src.common.time import timestamp_utc


class RuleModel(Base):
    def __init__(self):
        Base.__init__(self,RULE_COL_NAME)

    

    