import os
from flask import Flask, jsonify, render_template
from routes.expense_routes import expense_bp

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
    static_url_path="/static"
)

app.register_blueprint(expense_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
