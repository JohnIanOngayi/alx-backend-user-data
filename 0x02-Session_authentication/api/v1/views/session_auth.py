#!/usr/bin/env python3
"""
Module defines view that handles all routes for the Session auth
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Logs in a user
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users or not users[0] or not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    user = users[0]
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    from os import getenv

    cookie_name = getenv("SESSION_NAME")
    if cookie_name and session_id:
        resp.set_cookie(cookie_name, session_id)
    return resp


@app_views.route(
        "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Deletes current session hence logging out
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
