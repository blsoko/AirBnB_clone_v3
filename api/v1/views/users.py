#!/usr/bin/python3
""" RestApi request/response User Managment
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def getUserAll(user_id=None):
    """ Get User response
    """
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    else:
        listUsers = []
        storageUser = storage.all(User).values()
        for user in storageUser:
            listUsers.append(user.to_dict())
        return jsonify(listUsers)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delUser(user_id=None):
    """ Del User response
    """
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def postUser():
    """ make amenity post request
    """
    if request.get_json():
        if 'email' in request.get_json():
            if 'password' in request.get_json():
                data_Json = User(**request.get_json())
                data_Json.save()
                return make_response(jsonify(data_Json.to_dict()), 201)
            abort(400, description="Missing password")
        abort(400, description="Missing email")
    abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def putUser(user_id=None):
    """ Update amenity response
    """
    ignored_keys = ['id', 'created_at', 'updated_at', 'email']
    requested = request.get_json()

    if requested:
        user = storage.get(User, user_id)
        if user:
            for key, value in requested.items():
                if key not in ignored_keys:
                    setattr(user, key, value)
            user.save()
            return make_response(jsonify(user.to_dict()), 200)
        abort(404)
    abort(400, description="Not a JSON")
