from flask import Blueprint, jsonify, render_template
from database.connection import SessionLocal
from database.models import User
from utils.auth_middleware import token_required

users_bp = Blueprint("users", __name__)

# ----------------------------------------
# GET ALL USERS (OWNER ONLY)
# ----------------------------------------
@users_bp.get("/")
@token_required(["OWNER"])
def get_users():

    session = SessionLocal()

    users = session.query(User).all()

    data = []
    for u in users:
        data.append({
            "user_id": u.user_id,
            "username": u.username,
            "role": u.role.role_name
        })

    session.close()
    return jsonify(data)


# ----------------------------------------
# DELETE USER (OWNER ONLY)
# ----------------------------------------
@users_bp.delete("/<int:user_id>")
@token_required(["OWNER"])
def delete_user(user_id):

    session = SessionLocal()

    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404

    session.delete(user)
    session.commit()
    session.close()

    return jsonify({"message": "User deleted successfully"})

