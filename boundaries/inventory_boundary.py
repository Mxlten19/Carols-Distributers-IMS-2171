from flask import Blueprint, request, jsonify
from controls.inventory_control import InventoryService
from boundaries.auth_middleware import token_required

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.get("/")
@token_required(allowed_roles=["OWNER", "MANAGER", "CASHIER"])
def get_inventory():
    return jsonify(InventoryService.get_all_products())

@inventory_bp.post("/product")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def add_product():
    user_id = request.user["user_id"]   # ← extracted from token, not hardcoded
    return jsonify(InventoryService.add_product(request.json, user_id=user_id))

@inventory_bp.put("/product/<int:id>")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def update_product(id):
    user_id = request.user["user_id"]
    return jsonify(InventoryService.update_product(id, request.json, user_id=user_id))

@inventory_bp.delete("/product/<int:id>")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def delete_product(id):
    return jsonify(InventoryService.delete_product(id))

@inventory_bp.get("/categories")
@token_required(allowed_roles=["OWNER", "MANAGER", "CASHIER"])
def get_categories():
    return jsonify(InventoryService.get_all_categories())

@inventory_bp.post("/category")
@token_required(allowed_roles=["OWNER", "MANAGER"])
def add_category():
    return jsonify(InventoryService.add_category(request.json))