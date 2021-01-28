#!/usr/bin/python3
""" RestApi request/response Place Managment
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage
from models.place import Place
from models.city import City
from models.state import State


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def getPlaceAll(city_id=None):
    """ Get All Place response
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    listPlaces = []
    for key in city.places:
        listPlaces.append(key.to_dict())
    return jsonify(listPlaces)


@app_views.route("/places/<place_id>", methods=["GET"])
def getPlace(place_id=None):
    """ Get Place response
    """
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delPlace(place_id=None):
    """ Del Place response
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def postPlace(city_id=None):
    """ make Place post request
    """
    if request.get_json():
        city = storage.get(City, city_id)
        if city:
            if 'user_id' not in request.get_json():
                abort(400, description="Missing user_id")
            userRequest = request.get_json()
            user = storage.get(User, userRequest['user_id'])
            if not user:
                abort(404)
            if 'name' not in userRequest:
                abort(400, description="Missing name")
            userRequest["city_id"] = city_id
            data_Json = Place(**userRequest)
            data_Json.save()
            return make_response(jsonify(data_Json.to_dict()), 201)
        abort(404)
    abort(400, description="Not a JSON")


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def putPlace(place_id=None):
    """ Update Place response
    """
    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    requested = request.get_json()
    if requested:
        place = storage.get(Place, place_id)
        if place:
            for key, value in requested.items():
                if key not in ignored_keys:
                    setattr(place, key, value)
            place.save()
            return make_response(jsonify(place.to_dict()), 200)
        abort(404)
    abort(400, description="Not a JSON")
