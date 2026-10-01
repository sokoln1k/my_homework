import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_host = os.getenv("DB_HOST", "db")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "secret")
db_name = os.getenv("DB_NAME", "mydb")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Flask + Gunicorn + PostgreSQL in Docker"

@app.route("/check")
def check_db():
    try:
        db.session.execute("SELECT 1")
        return "DB connection OK"
    except Exception as e:
        return f"DB error: {e}", 500

if __name__ == "__main__":
    # Этот блок не используется при запуске через Gunicorn в Docker
    app.run(host="0.0.0.0", port=8000)
