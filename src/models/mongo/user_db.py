

from configs.configs import CONFIG_ACCOUNT_DB
from src.models.mongo.base import Base


class MGUser(Base):

    def __init__(self, col=None) -> None:
        super().__init__(col)
        # common format, need follow
        self.col = CONFIG_ACCOUNT_DB["users"]

    # def createM(payload, creator=None):
    #     return super().create(payload=payload, creator=creator)