from flask import Blueprint, jsonify
from database.connection import SessionLocal
from database.models import Alert
from utils.auth_middleware import token_required

alert_bp = Blueprint("alerts", __name__)

@alert_bp.get("/")
@token_required(allowed_roles=["OWNER","MANAGER"])
def get_alerts():
    session = SessionLocal()
    alerts = session.query(Alert).all()

    data = []
    for a in alerts:
        data.append({
            "id": a.alert_id,  # <-- needed for delete
            "product": a.product.name if a.product else "Unknown",
            "msg": a.message,
            "status": a.status,
            "created_at": (
                a.created_at.strftime("%Y-%m-%d %H:%M")
                if getattr(a, "created_at", None) else ""
            )
        })

    session.close()
    return jsonify(data)


@alert_bp.delete("/<int:alert_id>")
def delete_alert(alert_id):
    session = SessionLocal()
    alert = session.query(Alert).filter_by(alert_id=alert_id).first()

    if not alert:
        session.close()
        return jsonify({"error": "Alert not found"}), 404

    if alert.status != "RESOLVED":
        session.close()
        return jsonify({"error": "Only resolved alerts can be deleted"}), 400

    session.delete(alert)
    session.commit()
    session.close()

    return jsonify({"message": "Alert deleted successfully"})

