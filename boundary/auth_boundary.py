from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login_route():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    result = AuthService.login(username, password)
    return jsonify(result)
