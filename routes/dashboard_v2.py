from flask import Blueprint, render_template, jsonify

from modules.system.info import get_system_info


dashboard_v2 = Blueprint(
    "dashboard_v2",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_v2.route("/")
def index():

    return render_template(
        "index.html"
    )


@dashboard_v2.route("/api/status")
def status():

    return jsonify(
        get_system_info()
    )
