
import bson


def get_json_from_db(data):
    for key in data:
        if bson.ObjectId().is_valid(data[key]):
            data[key] = str(data[key])

    return data