import os
import sys
import traceback
from flask import Flask, jsonify, render_template
from routes.expense_routes import expense_bp

# Get the absolute path to frontend directories
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(base_dir), "frontend", "templates")
static_dir = os.path.join(os.path.dirname(base_dir), "frontend", "static")

print(f"DEBUG: base_dir = {base_dir}", file=sys.stderr)
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
        "template_exists": os.path.exists(template_dir),
        "static_exists": os.path.exists(static_dir)
    }), 200

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
