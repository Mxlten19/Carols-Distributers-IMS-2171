from flask import Flask, send_from_directory
from flask_cors import CORS
from config import SECRET_KEY
from boundaries.auth_boundary import auth_bp
from boundaries.inventory_boundary import inventory_bp
from boundaries.sales_boundary import sales_bp
from boundaries.alert_boundary import alert_bp
from boundaries.report_boundary import report_bp
from boundaries.user_boundary import users_bp
from entities.connection import Base, engine
from entities.models import Role, User, Category, Product, SaleTransaction, SaleItem, Alert
from controls.alert_control import AlertControl
from controls.report_control import init_report_scheduler
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = SECRET_KEY
CORS(app)

Base.metadata.create_all(engine)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(inventory_bp, url_prefix="/inventory")
app.register_blueprint(sales_bp, url_prefix="/sales")
app.register_blueprint(alert_bp, url_prefix="/alerts")
app.register_blueprint(report_bp, url_prefix="/reports")
app.register_blueprint(users_bp, url_prefix="/users")

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

with app.app_context():
    init_report_scheduler()
    AlertControl.check_all_products()

if __name__ == "__main__":
    app.run(debug=True)