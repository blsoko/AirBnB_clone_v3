#!/usr/bin/python3
""" RestApi request/response Places_reviews Managment
"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def getReviewAll(place_id=None):
    """ Get All Review response
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    listReview = []
    for key in place.reviews:
        listReview.append(key.to_dict())
    return jsonify(listReview)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def getReview(review_id=None):
    """ Get Review response
    """
    if review_id:
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delReview(review_id=None):
    """ Del Review response
    """
    place = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def postReview(place_id=None):
    """ make Review post request
    """
    if request.get_json():
        place = storage.get(Place, place_id)
        if place:
            if 'user_id' not in request.get_json():
                abort(400, description="Missing user_id")
            userRequest = request.get_json()
            user = storage.get(User, userRequest['user_id'])
            if not user:
                abort(404)
            if 'text' not in userRequest:
                abort(400, description="Missing text")
            userRequest["place_id"] = place_id
            data_Json = Review(**userRequest)
            data_Json.save()
            return make_response(jsonify(data_Json.to_dict()), 201)
        abort(404)
    abort(400, description="Not a JSON")


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def putReview(review_id=None):
    """ Update Review response
    """
    ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    requested = request.get_json()

    if requested:
        review = storage.get(Review, review_id)
        if review:
            for key, value in requested.items():
                if key not in ignored_keys:
                    setattr(review, key, value)
            review.save()
            return make_response(jsonify(review.to_dict()), 200)
        abort(404)
    abort(400, description="Not a JSON")
