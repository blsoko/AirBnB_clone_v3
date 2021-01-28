#!/usr/bin/python3
"""View for 'State' via API"""
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def view_states(state_id=None):
    """Returns a list of all State objects or just one per id"""
    if state_id:
        tmp = storage.get(State, state_id)
        if tmp is None:
            abort(404)
        return jsonify(tmp.to_dict())
    else:
        states = [val.to_dict() for val in storage.all(State).values()]
        return jsonify(states)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    tmp = storage.get(State, state_id)
    if tmp is None:
        abort(404)
    storage.delete(tmp)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """Make a POST request"""
    req = request.get_json()
    if req:
        if req.get('name'):
            new_state = State(**req)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State"""
    tmp = storage.get(State, state_id)
    if tmp is None:
        abort(404)
    else:
        req = request.get_json()
        if req:
            keys = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in keys:
                    setattr(tmp, key, value)
            tmp.save()
            return jsonify(tmp.to_dict()), 200
        else:
            abort(400, "Not a JSON")
