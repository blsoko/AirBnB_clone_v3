#!/usr/bin/python3
"""New view for the link between Place and Amenity via API"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route("places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def amenities_view_place(place_id):
    """Retrieves all Amenity objects of a Place"""
    tmp = storage.get(Place, place_id)
    if tmp is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        listamenities = [value.to_dict() for value in tmp.amenities]
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        listamenities = [storage.get(Amenity,
                                     val).to_dict() for val in tmp.amenity_ids]
    return jsonify(listamenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """Delete a Amenity object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if my_amenity not in my_place.amenities:
            abort(404)
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        if my_amenity.id not in my_place.amenity_ids:
            abort(404)
    storage.delete(my_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=['POST'], strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """Create a new Amenity object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)

    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if my_amenity in my_place.amenities:
            return jsonify(my_amenity.to_dict()), 200
        my_place.amenities.append(my_amenity)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        if my_amenity.id in my_place.amenity_ids:
            return jsonify(my_amenity.to_dict()), 200
        my_place.amenity_ids.append(my_amenity)

    return jsonify(my_amenity.to_dict()), 201
