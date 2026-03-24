from flask import Blueprint, request, jsonify
from services.sales_service import SalesService
from utils.auth_middleware import token_required
from flask import send_from_directory
import os

sales_bp = Blueprint("sales", __name__)

@sales_bp.post("/")
@token_required(allowed_roles=["OWNER","CASHIER"])
def make_sale():
    data = request.json

    return jsonify(
        SalesService.create_sale(
            cashier_id=data["cashier_id"],    
            items=data["items"]
        )
    )
# ------------------------------------
# VIEW / DOWNLOAD RECEIPTS
# ------------------------------------
@sales_bp.get("/receipt/<filename>")
@token_required(allowed_roles=["OWNER","CASHIER","MANAGER"])
def view_receipt(filename):

    # prevent path traversal
    if ".." in filename or "/" in filename:
        return jsonify({"error": "Invalid filename"}), 400

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RECEIPTS_DIR = os.path.join(BASE_DIR, "receipts")

    filepath = os.path.join(RECEIPTS_DIR, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "Receipt not found"}), 404

    download = request.args.get("download") == "true"

    return send_from_directory(
        directory=RECEIPTS_DIR,
        path=filename,
        mimetype="application/pdf",
        as_attachment=download 
    )