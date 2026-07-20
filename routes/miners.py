from flask import Blueprint, jsonify
from services.antminer_service import get_antminer_status

miners = Blueprint("miners", __name__)

@miners.route("/miners/status/<ip>", methods=["GET"])
def miner_status(ip):
    return jsonify(get_antminer_status(ip))
