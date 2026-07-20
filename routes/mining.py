from flask import Blueprint, jsonify

mining_routes = Blueprint("mining_routes", __name__)

@mining_routes.route("/mining/status")
def mining_status():
    return jsonify({
        "miner": "XMRig",
        "coin": "Monero",
        "algorithm": "RandomX",
        "pool": "2Miners",
        "status": "ready"
    })
