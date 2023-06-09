#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""

from functools import wraps

from flask import jsonify, Flask
from mobio.libs.logging import MobioLogging, LoggingConstant
from mobio.sdks.base.common import CONSTANTS
from mobio.sdks.base.common.lang_config import LangError
from mobio.sdks.base.common.mobio_exception import BaseMoError, DBLogicError, InputNotFoundError, LogicSystemError, \
    ParamInvalidError, CustomError, CustomUnauthorizeError, UnauthorizationError
from mobio.sdks.base.common.system_config import SystemConfig
from mobio.sdks.admin.http_jwt_auth import HttpJwtAuth
from mobio.sdks.admin.mobio_authorization import MobioAuthorization

from configs import AccountConfigApplicationConfig

sys_conf = SystemConfig()
app = Flask(AccountConfigApplicationConfig.NAME, static_folder=None)
auth = HttpJwtAuth(MobioAuthorization())


class HTTP:
    class METHOD:
        DELETE = 'delete'
        PATCH = 'patch'
        PUT = 'put'
        POST = 'post'
        GET = 'get'
        SUPPORTED = [GET, POST, PUT, PATCH, DELETE]

    class STATUS:
        OK = 200


def build_response_message(data=None):
    message = BaseMoError(LangError.MESSAGE_SUCCESS).get_message()
    log_mod = sys_conf.get_section_map(CONSTANTS.LOGGING_MODE)
    if int(log_mod[LoggingConstant.LOG_FOR_REQUEST_SUCCESS]) == 1:
        MobioLogging().debug('response: %s' % (data or message))

    result = message
    if data is not None:
        if isinstance(data, dict):
            result.update(data)
        else:
            result['data'] = data
    return result


# @app.errorhandler(400)
def bad_request(exception=None):
    if exception is None:
        exception = DBLogicError(LangError.BAD_REQUEST)
    return jsonify(exception.get_message()), 400

# @app.errorhandler(401)
def unauthor(exception=None):
    if exception is None:
        exception = UnauthorizationError(LangError.BAD_REQUEST)
    return jsonify(exception.get_message()), 401

# @app.errorhandler(404)
def not_found(exception=None):
    if exception is None:
        exception = InputNotFoundError(LangError.NOT_FOUND)
    return jsonify(exception.get_message()), 404

def unprocessable_content(exception=None):
    if exception is None:
        exception = ParamInvalidError(LangError.VALIDATE_ERROR)
    return jsonify(exception.get_message()), 422

# @app.errorhandler(405)
def not_allowed(exception=None):
    if exception is None:
        exception = LogicSystemError(LangError.NOT_ALLOWED)
    return jsonify(exception.get_message()), 405


# @app.errorhandler(412)
def param_invalid_error(exception):
    if exception is None:
        exception = ParamInvalidError(LangError.VALIDATE_ERROR)
    return jsonify(exception.get_message()), 412

def conflict(exception=None):
    if exception is None:
        exception = DBLogicError(LangError.ALREADY_EXIST)
    return jsonify(exception.get_message()), 409

# @app.errorhandler(413)
def custom_exception(exception=None):
    if exception is None:
        exception = CustomError(LangError.CUSTOM_ERROR)
    if len(exception.args) > 0:
        message = exception.args[0]
        if isinstance(message, dict):
            return jsonify(message), 413
    else:
        message = 'Custom Error! Please investigate'
    return jsonify({'code': 413, 'message': message}), 413


@app.errorhandler(401)
def unauthorized():
    mo = BaseMoError(LangError.UNAUTHORIZED)
    return jsonify(mo.get_message()), 401


@app.errorhandler(500)
def internal_server_error(e=None):
    print(e)
    mo = BaseMoError(LangError.INTERNAL_SERVER_ERROR)
    return jsonify(mo.get_message()), 500


def try_catch_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return jsonify(f(*args, **kwargs)), 200
        except ParamInvalidError as pie:
            return param_invalid_error(pie)
        except InputNotFoundError as inf:
            return not_found(inf)
        except LogicSystemError as lse:
            return not_allowed(lse)
        except DBLogicError as dbe:
            return bad_request(dbe)
        except CustomError as ce:
            return custom_exception(ce)
        except CustomUnauthorizeError:
            return unauthorized()
        except Exception as e:
            return internal_server_error(e)

    return decorated

def response_message(data=None):
    message = BaseMoError(LangError.MESSAGE_SUCCESS).get_message()
    log_mod = sys_conf.get_section_map(CONSTANTS.LOGGING_MODE)
    if int(log_mod[LoggingConstant.LOG_FOR_REQUEST_SUCCESS]) == 1:
        MobioLogging().debug('response: %s' % (data or message))
 
    response = {
        "code": 200,
        "message": message["message"],
        "lang": message["lang"],
        "data": data
    }
    

    return jsonify(response),200
