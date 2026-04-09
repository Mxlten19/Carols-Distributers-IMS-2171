from entities.connection import SessionLocal
from entities.models import User, Role
from controls.password_hash import hash_password
from datetime import datetime, timedelta

class UserControl:

    @staticmethod
    def get_all_users():
        session = SessionLocal()
        users = session.query(User).all()
        result = []
        for u in users:
            is_deactivated = (
                u.locked_until is not None and
                u.locked_until > datetime.utcnow() and
                u.failed_attempts == 999
            )
            result.append({
                "user_id": u.user_id,
                "username": u.username,
                "role": u.role.role_name if u.role else "N/A",
                "role_id": u.role_id,
                "status": "DEACTIVATED" if is_deactivated else "ACTIVE"
            })
        session.close()
        return result

    @staticmethod
    def get_all_roles():
        session = SessionLocal()
        roles = session.query(Role).all()
        data = [{"role_id": r.role_id, "role_name": r.role_name} for r in roles]
        session.close()
        return data

    @staticmethod
    def add_user(data):
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        role_id  = data.get("role_id")

        if not username or not password or not role_id:
            return {"error": "Username, password and role are required"}
        if len(password) < 6:
            return {"error": "Password must be at least 6 characters"}

        session = SessionLocal()
        if session.query(User).filter_by(username=username).first():
            session.close()
            return {"error": "Username already exists"}
        if not session.query(Role).filter_by(role_id=role_id).first():
            session.close()
            return {"error": "Invalid role selected"}

        session.add(User(
            username=username,
            password_hash=hash_password(password),
            role_id=role_id,
            failed_attempts=0
        ))
        session.commit()
        session.close()
        return {"message": f"User '{username}' created successfully"}

    @staticmethod
    def edit_user(user_id, data):
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            session.close()
            return {"error": "User not found"}

        if "username" in data and data["username"].strip():
            new_username = data["username"].strip()
            existing = session.query(User).filter_by(username=new_username).first()
            if existing and existing.user_id != user_id:
                session.close()
                return {"error": "Username already taken"}
            user.username = new_username

        if "password" in data and data["password"].strip():
            if len(data["password"]) < 6:
                session.close()
                return {"error": "Password must be at least 6 characters"}
            user.password_hash = hash_password(data["password"])

        if "role_id" in data:
            if not session.query(Role).filter_by(role_id=data["role_id"]).first():
                session.close()
                return {"error": "Invalid role"}
            user.role_id = data["role_id"]

        session.commit()
        session.close()
        return {"message": "User updated successfully"}

    @staticmethod
    def deactivate_user(user_id):
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            session.close()
            return {"error": "User not found"}
        user.locked_until = datetime.utcnow() + timedelta(days=36500)
        user.failed_attempts = 999
        session.commit()
        session.close()
        return {"message": f"User '{user.username}' has been deactivated"}

    @staticmethod
    def reactivate_user(user_id):
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            session.close()
            return {"error": "User not found"}
        user.locked_until = None
        user.failed_attempts = 0
        session.commit()
        session.close()
        return {"message": f"User '{user.username}' has been reactivated"}

    @staticmethod
    def delete_user(user_id):
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            session.close()
            return {"error": "User not found"}
        session.delete(user)
        session.commit()
        session.close()
        return {"message": "User deleted successfully"}