from src.models.mongo.base import Base
from configs.configs import USER_COL_NAME


class UserModel(Base):
    def __init__(self):
        Base.__init__(self, USER_COL_NAME)
        
#     def find_user_by_name(self, name):
#         query = {"name": name}
#         users = self.collection.find(query)
#         return list(users)