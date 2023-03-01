import os
os.environ["HOST"] = "https://api-test1.mobio.vn/"
os.environ["ADMIN_HOST"]="https://api-test1.mobio.vn"
os.environ["APPLICATION_DATA_DIR"]="/home/toan/Desktop/Redis/AccountConfig"
os.environ["APPLICATION_LOGS_DIR"]="/home/toan/Desktop/Redis/AccountConfig"
os.environ["ACCOUNT_CONFIG_HOME"]="/home/toan/Desktop/Redis/AccountConfig"


#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""
from flask_cors import CORS
from src.apis.v1_0 import *


CORS(app)
"""
@api {get} /user/:id Request User information
@apiName GetUser
@apiGroup User

@apiParam {Number} id Users unique ID.

@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
