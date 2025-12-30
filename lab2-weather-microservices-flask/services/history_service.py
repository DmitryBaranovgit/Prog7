from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "history.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
                     city TEXT
        )
        """)

@app.route("/history", methods=["POST"])
def save_history():
    city = request.json.get("city")
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO history (city) VALUES (?)", (city,))
    return jsonify({"status": "saved"})

@app.route("/stats")
def stats():
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
        SELECT city, COUNT(*) as cnt
        FROM history
        GROUP BY city
        ORDER BY cnt DESC
        """)
        result = [{"city": r[0], "count": r[1]} for r in cursor.fetchall()]
    return jsonify(result)

init_db()