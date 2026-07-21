from flask import Blueprint, jsonify

from modules.system.info import get_system_info


system = Blueprint(
    "system",
    __name__,
    url_prefix="/system"
)


@system.route("/info", methods=["GET"])
def system_info():

    data = get_system_info()

    return jsonify({
        "status": "success",
        "data": data
    })


@system.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "online",
        "service": "Builder_House",
        "module": "system"
    })
