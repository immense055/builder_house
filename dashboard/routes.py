from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
def home():
    return render_template("dashboard.html")

@dashboard.route("/dashboard/login")
def login():
    return render_template("login.html")

@dashboard.route("/dashboard/register")
def register():
    return render_template("register.html")

@dashboard.route("/dashboard/docs")
def docs():
    return render_template("docs.html")

@dashboard.route("/dashboard/api-keys")
def api_keys():
    return render_template("api_keys.html")
