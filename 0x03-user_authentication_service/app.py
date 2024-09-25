#!/usr/bin/env python3

"""Module defines basic Flask app"""

from flask import abort, Flask, jsonify, make_response, redirect, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """GET /
    returns a success JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """POST /users
    registers user into the database"""
    json = request.form.to_dict()
    email = json.get("email")
    password = json.get("password")
    if not email or not password:
        return None
    try:
        new_user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    if new_user:
        return jsonify(
                {"email": f"{new_user.email}", "message": "user created"}
                )


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions
    validates and logs in user"""
    json = request.form.to_dict()
    email = json.get("email")
    password = json.get("password")
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        resp = make_response(jsonify(
            {"email": f"{email}", "message": "logged in"})
            )
        session_id = AUTH.create_session(email)
        if session_id:
            resp.set_cookie("session_id", session_id)
            return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """DELETE /sessions
    logs out user by deleting session in db"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(location="/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def fetch_profile():
    """GET /profile
    finds and returns current User email"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
