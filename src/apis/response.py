from flask import jsonify

def success(data = None, message = 'Thành công'):
    response = {
        "code": 200,
        "message": message,
        "data": data
    }
    return jsonify(response),200

def bad_request(message= "Yêu cầu không hợp lệ"):
    response = {
        "code": 400,
        "message": message,
    }
    return jsonify(response), 400

def not_found(message = "Không tìm thấy mục nào"):
    response = {
        "code": 404,
        "message": message,
    }
    return jsonify(response), 404