
import json


def get_json_from_mongo(data):
    return json.loads(json.dumps(data, default=str))
