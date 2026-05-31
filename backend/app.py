import os
import sys
import traceback
from flask import Flask, jsonify, render_template
from routes.expense_routes import expense_bp
from database.db import expenses, users

# Determine the correct paths - backend is in /backend, frontend is in /frontend at repo root
# __file__ = /backend/app.py
# os.path.abspath(__file__) = /full/path/to/backend/app.py
# os.path.dirname(...) = /full/path/to/backend
# os.path.dirname(dirname) = /full/path/to/repo/root

backend_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(backend_dir)
template_dir = os.path.join(repo_root, "frontend", "templates")
static_dir = os.path.join(repo_root, "frontend", "static")

print(f"DEBUG: backend_dir = {backend_dir}", file=sys.stderr)
print(f"DEBUG: repo_root = {repo_root}", file=sys.stderr)
print(f"DEBUG: template_dir = {template_dir}", file=sys.stderr)
print(f"DEBUG: static_dir = {static_dir}", file=sys.stderr)
print(f"DEBUG: template_dir exists = {os.path.exists(template_dir)}", file=sys.stderr)
print(f"DEBUG: static_dir exists = {os.path.exists(static_dir)}", file=sys.stderr)
if os.path.exists(template_dir):
    print(f"DEBUG: templates = {os.listdir(template_dir)}", file=sys.stderr)
if os.path.exists(static_dir):
    print(f"DEBUG: static files = {os.listdir(static_dir)}", file=sys.stderr)

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,
    static_url_path="/static"
)

app.register_blueprint(expense_bp)

@app.route("/health")
def health():
    """Health check endpoint that doesn't require database"""
    return jsonify({
        "status": "ok",
        "backend_dir": backend_dir,
        "repo_root": repo_root,
        "template_dir": template_dir,
        "static_dir": static_dir,
        "template_exists": os.path.exists(template_dir),
        "static_exists": os.path.exists(static_dir),
        "repo_root_contents": os.listdir(repo_root) if os.path.exists(repo_root) else []
    }), 200


@app.route("/dbcheck")
def dbcheck():
    """Database connectivity check - returns users count or error details."""
    try:
        if users is None or expenses is None:
            return jsonify({"status": "error", "message": "Database not initialized"}), 503

        # perform a lightweight operation
        users_count = users.count_documents({})
        expenses_count = expenses.count_documents({})
        return jsonify({
            "status": "ok",
            "users_count": int(users_count),
            "expenses_count": int(expenses_count)
        }), 200
    except Exception as e:
        import traceback as _tb
        _tb.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"ERROR rendering template: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"ERROR 500: {str(error)}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return jsonify({"message": "Internal server error", "error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
