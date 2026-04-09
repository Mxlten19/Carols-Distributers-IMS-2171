from flask import Blueprint, jsonify
from controls.alert_control import AlertControl
from boundaries.auth_middleware import token_required

alert_bp = Blueprint("alerts", __name__)

@alert_bp.get("/")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def get_alerts():
    return jsonify(AlertControl.get_all_alerts())

@alert_bp.delete("/<int:alert_id>")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def delete_alert(alert_id):
    result, status = AlertControl.delete_alert(alert_id)
    return jsonify(result), status