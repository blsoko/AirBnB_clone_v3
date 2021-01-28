#!/usr/bin/python3
""" RestApi request/response City Managment
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def getCityAll(state_id=None):
    """ Get all cities response
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    listCities = []
    for key in state.cities:
        listCities.append(key.to_dict())
    return jsonify(listCities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def getCity(city_id=None):
    """ Get city response
    """
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delCity(city_id=None):
    """ Del city response
    """
    city = storage.get(City, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def postCity(state_id=None):
    """ Make a city post request
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.get_json():
        if 'name' in request.get_json():
            data_Json = City(**request.get_json())
            data_Json.state_id = state_id
            data_Json.save()
            return make_response(jsonify(data_Json.to_dict()), 201)
        abort(400, description="Missing name")
    abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def putCity(city_id=None):
    """ Update a city request
    """
    ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
    requested = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if requested:
        for key, value in requested.items():
            if key not in ignored_keys:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
    abort(400, description="Not a JSON")
