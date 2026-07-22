from flask import Blueprint, render_template

recovery = Blueprint(
    "recovery",
    __name__,
    url_prefix="/recovery"
)

@recovery.route("/")
def index():
    return {
        "module": "Recovery",
        "status": "online"
    }

@recovery.route("/dashboard")
def dashboard():
    return render_template("recovery_dashboard.html")
