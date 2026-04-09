from entities.connection import SessionLocal
from entities.models import User
from controls.password_hash import verify_password
from controls.jwt_helper import create_token
from datetime import datetime, timedelta


class AuthService:

    MAX_ATTEMPTS = 3
    LOCK_TIME = timedelta(seconds=60)


    @staticmethod
    def login(username, password):

        now = datetime.utcnow()
        session = SessionLocal()

        try:
            user = session.query(User).filter_by(username=username).first()

            # -------------------------
            # USER NOT FOUND
            # -------------------------
            if not user:
                return {
                    "error": "Invalid username or password."
                }

            # -------------------------
            # LOCK CHECK
            # -------------------------
            if user.locked_until and user.locked_until > now:

                seconds_left = int(
                    (user.locked_until - now).total_seconds()
                )

                return {
                    "error": "Too many failed attempts. Try again later.",
                    "locked": True,
                    "seconds_left": seconds_left
                }

            # -------------------------
            # INVALID PASSWORD
            # -------------------------
            if not verify_password(password, user.password_hash):

                user.failed_attempts += 1

                # LOCK ACCOUNT IF LIMIT HIT
                if user.failed_attempts >= AuthService.MAX_ATTEMPTS:
                    user.locked_until = now + AuthService.LOCK_TIME

                    session.commit()

                    return {
                        "error": "Account locked for 60 seconds.",
                        "locked": True,
                        "seconds_left": 60
                    }

                session.commit()

                return {
                    "error": "Invalid username or password.",
                    "attempts_left": AuthService.MAX_ATTEMPTS - user.failed_attempts
                }

            # -------------------------
            # SUCCESSFUL LOGIN
            # -------------------------
            user.failed_attempts = 0
            user.locked_until = None
            session.commit()

            token = create_token(
                user.user_id,
                user.role.role_name
            )

            return {
                "token": token,
                "role": user.role.role_name,
                "username": user.username
                "user_id": user.user_id
            }

        finally:
            session.close()
