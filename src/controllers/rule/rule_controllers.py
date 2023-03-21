from flask import request
from src.models.mongo.rule_model import RuleModel
from bson.objectid import ObjectId
from mobio.libs.logging import MobioLogging


class RuleControllers():
    def __init__(self):
        pass

    def validate_add_rule(self, input_data):
        pass

    def add_rule(self):
        body_data = request.get_json()
        self.validate_add_rule(body_data)
        rule = {
            "name": body_data["name"],
            "status": body_data["status"]
        }

        # Fake cretor
        cretor = ObjectId()

        RuleModel().create(rule, cretor)
        MobioLogging().info("Update rule success")

        return body_data

    def get_all(self):
        return {"all": "Rules"}
    


