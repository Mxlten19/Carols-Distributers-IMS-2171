from entities.connection import SessionLocal
from entities.models import Product, Category
from controls.alert_control import AlertControl
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class InventoryControl:

    # ------------------------------------------------------------
    # GET ALL PRODUCTS
    # ------------------------------------------------------------
    @staticmethod
    def get_all_products():
        session = SessionLocal()
        products = session.query(Product).all()

        data = []
        for p in products:
            data.append({
                "product_id": p.product_id,          # DB numeric id
                "id": p.code,                        # Custom display ID: BEV_001
                "name": p.name,
                "category": p.category.name if p.category else "",
                "price": p.price,
                "qty": p.current_quantity,
                "reorder_threshold": p.reorder_threshold
            })

        session.close()
        return data


    # ------------------------------------------------------------
    # GET ALL CATEGORIES
    # ------------------------------------------------------------
    @staticmethod
    def get_all_categories():
        session = SessionLocal()
        categories = session.query(Category).order_by(Category.name).all()

        data = [{"id": c.category_id, "name": c.name} for c in categories]

        session.close()
        return data


    # ------------------------------------------------------------
    # ADD PRODUCT
    # Generates product IDs like BEV_001, BEV_002, FOO_001, etc.
    # ------------------------------------------------------------
    

    @staticmethod
    def add_product(data, user_id):
        session = SessionLocal()

        name = data.get("name")
        category_name = data.get("category")
        price = data.get("price")
        qty = data.get("quantity")
        threshold = data.get("reorder_threshold")

        # ---- Validation ----
        if not name or price is None or qty is None or not category_name:
            session.close()
            return {"error": "Missing required fields"}

        try:
            threshold = int(threshold)
        except (TypeError, ValueError):
            threshold = 0

        # ---- Validate category ----
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            session.close()
            return {"error": "Invalid category selected"}

        prefix = category.code_prefix

        last_product = (
            session.query(Product)
            .filter(Product.category_id == category.category_id)
            .filter(Product.code.like(f"{prefix}_%"))
            .order_by(Product.product_id.desc())
            .first()
        )

        if last_product:
            try:
                last_number = int(last_product.code.split("_")[-1])
            except:
                last_number = 0
        else:
            last_number = 0

        next_number = last_number + 1
        code = f"{prefix}_{str(next_number).zfill(3)}"

        product = Product(
            name=name,
            category_id=category.category_id,
            price=price,
            current_quantity=qty,
            reorder_threshold=threshold,
            code=code,
            updated_by_user_id=user_id
        )

        session.add(product)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            session.close()
            return {"error": "A product with that name already exists."}

        # ---- Alert check ----
        AlertControl.check_low_stock(product.product_id)

        session.close()
        return {
            "message": "Product added successfully",
            "product_code": code
        }


    # ------------------------------------------------------------
    # UPDATE PRODUCT
    # ------------------------------------------------------------
    @staticmethod
    def update_product(product_id, data, user_id):
        session = SessionLocal()

        product = (
            session
            .query(Product)
            .filter_by(product_id=product_id)
            .first()
        )

        if not product:
            session.close()
            return {"error": "Product not found"}

        # ---- Handle category ----
        if "category" in data:
            category_name = data["category"]

            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                session.close()
                return {"error": "Invalid category selected"}

            product.category_id = category.category_id


        # ---- Field updates ----
        if "name" in data:
            product.name = data["name"]

        if "price" in data:
            product.price = data["price"]

        if "current_quantity" in data:
            try:
                product.current_quantity = int(data["current_quantity"])
            except:
                pass

        if "reorder_threshold" in data:
            try:
                product.reorder_threshold = int(data["reorder_threshold"])
            except:
                pass

        product.updated_at = datetime.utcnow()
        product.updated_by_user_id = user_id

        session.commit()

        # ---- Alert check ----

        AlertControl.check_low_stock(product.product_id)

        session.close()
        return {"message": "Product updated successfully"}


    # ------------------------------------------------------------
    # DELETE PRODUCT
    # ------------------------------------------------------------
    @staticmethod
    def delete_product(product_id):
        session = SessionLocal()

        product = session.query(Product).filter_by(product_id=product_id).first()

        if not product:
            session.close()
            return {"error": "Product not found"}

        from entities.models import SaleItem, Alert
        
        # check if product has sale history
        has_sales = session.query(SaleItem).filter_by(product_id=product_id).first()
        if has_sales:
            session.close()
            return {"error": f"Cannot delete '{product.name}' — it has existing sales records. Deactivate it instead by setting quantity to 0."}

        # delete any alerts linked to this product first
        session.query(Alert).filter_by(product_id=product_id).delete()

        session.delete(product)
        session.commit()
        session.close()

        return {"message": "Product deleted successfully"}