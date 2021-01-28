#!/usr/bin/python3
"""View for City objects via API"""
from flask import Flask, make_response, request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities_view(state_id):
    """
    Retrieves the list of all State objects
    """
    tmp = storage.get(State, state_id)
    if tmp is None:
        abort(404)
    cty = [value.to_dict() for value in tmp.cities]
    return jsonify(cty)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def view_cities(city_id):
    """Retrieves all state objects"""
    tmp = storage.get(City, cities_id)
    if tmp is None:
        abort(404)
    return jsonify(tmp.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """Deletes a City object"""
    tmp = storage.get(City, cities_id)
    if tmp is None:
        abort(404)
    storage.delete(tmp)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def post_cities(state_id=None):
    """Create a City"""
    content = request.get_json()
    if content:
        if content.get('name'):
            new_city = City(**content)
            new_city.state_id = state_id
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    tmp = storage.get(City, city_id)
    if tmp is None:
        abort(404)
    else:
        req = request.get_json()
        if req:
            keys = ['id', 'created_at', 'updated_at', "state_id"]
            for key, value in req.items():
                if key not in keys:
                    setattr(tmp, key, value)
            tmp.save()
            return jsonify(tmp.to_dict()), 200
        else:
            abort(400, "Not a JSON")
