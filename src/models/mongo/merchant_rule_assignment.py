
from configs.configs import CONFIG_ACCOUNT_DB
from src.models.mongo.base import Base


class MGMerchantRuleAssignment(Base):

    def __init__(self, col=None) -> None:
        super().__init__(col)
        # common format, need follow
        self.col = CONFIG_ACCOUNT_DB["merchant_rule_assignments"]
