import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

# Import the app from backend.app module
import importlib.util
backend_app_path = os.path.join(os.path.dirname(__file__), "backend", "app.py")
spec = importlib.util.spec_from_file_location("backend_app", backend_app_path)
backend_app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_app_module)
app = backend_app_module.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
