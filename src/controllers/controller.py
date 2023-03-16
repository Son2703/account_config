# from flask import Blueprint, render_template, abort,jsonify
# from jinja2 import TemplateNotFound

# simple_page = Blueprint('simple_page', __name__,
#                         template_folder='templates')

# @simple_page("/user/:id", methods= ["GET"])
# def print():
#     """
#     @api {get} /user/:id Request User information
#     @apiName GetUser
#     @apiGroup User

#     @apiParam {Number} id Users unique ID.

#     @apiSuccess {String} firstname Firstname of the User hahah.
#     @apiSuccess {String} lastname  Lastname of the User.
#     """

#     return jsonify({"code": "haha"}), 200
# @simple_page("/user/haha", medthods=["GET"])
# def print2():
#     return render_template('apidoc/index.html')