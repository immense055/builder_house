from flask import Blueprint, jsonify
from modules.system.info import get_system_info

system_bp = Blueprint("system", __name__)

@system_bp.route("/api/system")
def system():
    return jsonify(get_system_info())
