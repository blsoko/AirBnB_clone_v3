#!/usr/bin/python3
"""View for City objects via API"""
from flask import Flask, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/cities", methods=['GET'], strict_slashes=False)
@app_views.route("/cities/<cities_id>", methods=['GET'], strict_slashes=False)
def view_cities(cities_id=None):
    """Retrieves all state objects"""
    if cities_id:
        tmp = storage.get(City, cities_id)
        if tmp is None:
            abort(404)
        return jsonify(tmp.to_dict())
    else:
        cities = [val.to_dict() for val in storage.all(City).values()]
        return jsonify(cities)


@app_views.route("/cities/<cities_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(cities_id):
    """Deletes a City object"""
    tmp = storage.get(City, cities_id)
    if tmp is None:
        abort(404)
    storage.delete(tmp)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities", methods=['POST'], strict_slashes=False)
def post_cities():
    """Create a City"""
    content = request.get_json()
    if content:
        if content.get('name'):
            new_city = State(**content)
            bew_city.state_id = state_id
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
