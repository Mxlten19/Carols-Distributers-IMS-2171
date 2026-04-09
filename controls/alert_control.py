from entities.connection import SessionLocal
from entities.models import Alert

class AlertControl:

    @staticmethod
    def get_all_alerts():
        session = SessionLocal()
        alerts = session.query(Alert).all()
        data = [{
            "id": a.alert_id,
            "product": a.product.name if a.product else "Unknown",
            "msg": a.message,
            "status": a.status,
            "created_at": (
                a.created_at.strftime("%Y-%m-%d %H:%M")
                if getattr(a, "created_at", None) else ""
            )
        } for a in alerts]
        session.close()
        return data

    @staticmethod
    def delete_alert(alert_id):
        session = SessionLocal()
        alert = session.query(Alert).filter_by(alert_id=alert_id).first()
        if not alert:
            session.close()
            return {"error": "Alert not found"}, 404
        if alert.status != "RESOLVED":
            session.close()
            return {"error": "Only resolved alerts can be deleted"}, 400
        session.delete(alert)
        session.commit()
        session.close()
        return {"message": "Alert deleted successfully"}, 200