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
    app.run(host='0.0.0.0', port=8000, debug=True)
