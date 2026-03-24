from database.connection import SessionLocal
from database.models import Alert, Product

class AlertService:


    @staticmethod
    def check_low_stock(product_id):
        session = SessionLocal()

        try:
            product = session.query(Product).filter_by(product_id=product_id).first()
            if not product:
                return

            # Find ANY existing alert for this product
            alert = session.query(Alert).filter_by(
                product_id=product.product_id,
                alert_type="LOW_STOCK"
            ).first()

            is_low = product.current_quantity <= product.reorder_threshold

            # ----------------------------
            # CREATE OR ACTIVATE ALERT
            # ----------------------------
            if is_low:

                if not alert:
                    # Create new alert if none exists
                    alert = Alert(
                        product_id=product.product_id,
                        alert_type="LOW_STOCK"
                    )
                    session.add(alert)

                # Always update message + status
                alert.message = f"{product.name} low stock ({product.current_quantity} left)"
                alert.status = "ACTIVE"

            # ----------------------------
            # RESOLVE ALERT
            # ----------------------------
            else:
                if alert:
                    alert.status = "RESOLVED"

            session.commit()

        finally:
            session.close()



    @staticmethod
    def check_all_products():
        session = SessionLocal()

        products = session.query(Product).all()

        session.close()

        for p in products:
            AlertService.check_low_stock(p.product_id)

