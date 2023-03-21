from src.models.mongo.base import Base
from configs.configs import RULE_COL_NAME

class RuleModel(Base):
    def __init__(self):
        Base.__init__(self,RULE_COL_NAME)

    