import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
from sqlalchemy import text
from config import app, db

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Optional: Disable track_modifications warning if you don't need it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional: Set default port if not set
port_number = int(os.environ.get("APP_PORT", 5153))

@app.route("/health_check")
def health_check():
    return "ok"

@app.route("/readiness_check")
def readiness_check():
    try:
        # Test database connection by querying for the tokens table count
        count = db.session.execute(text("SELECT COUNT(*) FROM tokens")).scalar()
        if count is None:
            raise ValueError("Database query returned no result.")
    except Exception as e:
        app.logger.error(f"Readiness check failed: {e}")
        return jsonify({"error": "failed to connect to the database"}), 500
    else:
        return "ok"

def get_daily_visits():
    with app.app_context():
        try:
            result = db.session.execute(text(""" 
                SELECT Date(created_at) AS date,
                    Count(*) AS visits
                FROM   tokens
                WHERE  used_at IS NOT NULL
                GROUP  BY Date(created_at)
            """))
            response = {str(row[0]): row[1] for row in result}
            app.logger.info(f"Daily visits: {response}")
            return response
        except Exception as e:
            app.logger.error(f"Error in get_daily_visits: {e}")
            return {"error": "Failed to fetch daily visits"}, 500

@app.route("/api/reports/daily_usage", methods=["GET"])
def daily_visits():
    return jsonify(get_daily_visits())

@app.route("/api/reports/user_visits", methods=["GET"])
def all_user_visits():
    try:
        result = db.session.execute(text(""" 
            SELECT t.user_id,
                t.visits,
                users.joined_at
            FROM   (SELECT tokens.user_id,
                        Count(*) AS visits
                    FROM   tokens
                    GROUP  BY user_id) AS t
                LEFT JOIN users
                        ON t.user_id = users.id;
        """))
        response = {row[0]: {"visits": row[1], "joined_at": str(row[2])} for row in result}
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error in all_user_visits: {e}")
        return jsonify({"error": "Failed to fetch user visits"}), 500

# Scheduler to fetch daily visits
scheduler = BackgroundScheduler()
job = scheduler.add_job(get_daily_visits, 'interval', seconds=30)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port_number)