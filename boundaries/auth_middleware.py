from functools import wraps
from flask import request, jsonify
from controls.jwt_helper import decode_token

def token_required(allowed_roles=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            token = None

            #  Try header
            auth_header = request.headers.get("Authorization")
            if auth_header:
                try:
                    token = auth_header.split(" ")[1]
                except:
                    pass

            #  Try query param for PDFs
            if not token:
                token = request.args.get("token")

            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                data = decode_token(token)
            except:
                return jsonify({"error": "Invalid token"}), 401

            # Role check
            if allowed_roles and data["role"] not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403

            request.user = data

            return fn(*args, **kwargs)

        return wrapper
    return decorator

