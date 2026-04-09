from flask import Blueprint, jsonify, request
from controls.user_control import UserControl
from boundaries.auth_middleware import token_required

users_bp = Blueprint("users", __name__)

@users_bp.get("/")
@token_required(["OWNER"])
def get_users():
    return jsonify(UserControl.get_all_users())

@users_bp.get("/roles")
@token_required(["OWNER"])
def get_roles():
    return jsonify(UserControl.get_all_roles())

@users_bp.post("/")
@token_required(["OWNER"])
def add_user():
    return jsonify(UserControl.add_user(request.get_json() or {}))

@users_bp.put("/<int:user_id>")
@token_required(["OWNER"])
def edit_user(user_id):
    return jsonify(UserControl.edit_user(user_id, request.get_json() or {}))

@users_bp.put("/<int:user_id>/deactivate")
@token_required(["OWNER"])
def deactivate_user(user_id):
    return jsonify(UserControl.deactivate_user(user_id))

@users_bp.put("/<int:user_id>/reactivate")
@token_required(["OWNER"])
def reactivate_user(user_id):
    return jsonify(UserControl.reactivate_user(user_id))

@users_bp.delete("/<int:user_id>")
@token_required(["OWNER"])
def delete_user(user_id):
    return jsonify(UserControl.delete_user(user_id))