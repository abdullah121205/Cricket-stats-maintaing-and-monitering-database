import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.db import Database
from backend.routes.players import players_bp
from backend.routes.teams import teams_bp
from backend.routes.matches import matches_bp
from backend.routes.venues import venues_bp
from backend.routes.stats import stats_bp

def create_app():
    app = Flask(__name__, static_folder=str(BASE_DIR / "frontend"))
    CORS(app)

    with app.app_context():
        try:
            Database.init_db()
        except Exception as e:
            print(f"[App Init Warning] DB initialization error: {e}")

    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(venues_bp)
    app.register_blueprint(stats_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/players")
    def players_page():
        return send_from_directory(app.static_folder, "players.html")

    @app.route("/teams")
    def teams_page():
        return send_from_directory(app.static_folder, "teams.html")

    @app.route("/matches")
    def matches_page():
        return send_from_directory(app.static_folder, "matches.html")

    @app.route("/statistics")
    def statistics_page():
        return send_from_directory(app.static_folder, "statistics.html")

    @app.route("/<path:path>")
    def static_proxy(path):
        file_path = BASE_DIR / "frontend" / path
        if file_path.exists():
            return send_from_directory(app.static_folder, path)
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "message": "Internal server error", "details": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    print(f"\n==========================================================")
    print(f" 🏏 Cricket Statistics Management System Server Started")
    print(f" URL: http://localhost:{Config.PORT}")
    print(f" Database Mode: {Database._engine.upper()}")
    print(f"==========================================================\n")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
