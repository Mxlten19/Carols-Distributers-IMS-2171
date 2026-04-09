from entities.connection import SessionLocal
from entities.models import Alert, Product

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

    @staticmethod
    def check_low_stock(product_id):
        session = SessionLocal()
        product = session.query(Product).filter_by(product_id=product_id).first()
        if not product:
            session.close()
            return

        if product.current_quantity <= product.reorder_threshold:
            existing = session.query(Alert).filter_by(
                product_id=product_id, status="active"
            ).first()
            if not existing:
                alert = Alert(
                    product_id=product_id,
                    alert_type="LOW_STOCK",
                    message=f"{product.name} is low on stock (Qty: {product.current_quantity})",
                    status="active"
                )
                session.add(alert)
                session.commit()
        session.close()

    @staticmethod
    def check_all_products():
        session = SessionLocal()
        products = session.query(Product).all()
        ids = [p.product_id for p in products]
        session.close()
        for pid in ids:
            AlertControl.check_low_stock(pid)