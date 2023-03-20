
import bson


def get_json_from_db(data):
    for key in data:
        if bson.ObjectId().is_valid(data[key]):
            data[key] = str(data[key])

    return data

def get_str_from_id(data):
    for v in data:
        v = get_json_from_db(v)
    return data