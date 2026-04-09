from flask import Blueprint, request, jsonify
from controls.auth_control import AuthControl

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login_route():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    result = AuthControl.login(username, password)
    return jsonify(result)
