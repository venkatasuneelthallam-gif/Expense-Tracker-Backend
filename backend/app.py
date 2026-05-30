import os
from flask import Flask, jsonify, render_template
from routes.expense_routes import expense_bp

# Get the absolute path to frontend directories
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(base_dir), "frontend", "templates")
static_dir = os.path.join(os.path.dirname(base_dir), "frontend", "static")

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,
    static_url_path="/static"
)

app.register_blueprint(expense_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
