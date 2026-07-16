from functools import wraps
from flask import jsonify

def admin_required(f):
    @wraps(f)
    def decorated(user_data, *args, **kwargs):

        if user_data.get("role") != "admin":
            return jsonify({
                "error": "Admin access required"
            }), 403

        return f(user_data, *args, **kwargs)

    return decorated
