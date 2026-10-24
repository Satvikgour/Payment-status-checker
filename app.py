import os
from flask import Flask, jsonify
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://payments:payments_dev_password@db:5432/payments"
)

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id VARCHAR(40) PRIMARY KEY,
                amount NUMERIC(10, 2) NOT NULL,
                currency VARCHAR(3) NOT NULL DEFAULT 'INR',
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        conn.execute("""
            INSERT INTO payments (payment_id, amount, currency, status)
            VALUES
                ('PAY1001', 500.00, 'INR', 'PENDING'),
                ('PAY1002', 1250.00, 'INR', 'SUCCESS'),
                ('PAY1003', 250.00, 'INR', 'FAILED')
            ON CONFLICT (payment_id) DO NOTHING
        """)

@app.get("/")
def home():
    return jsonify({
        "service": "Payment Status Checker API",
        "message": "Use /health or /payments/<payment_id>"
    })

@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "unavailable"}), 503

@app.get("/payments/<payment_id>")
def payment_status(payment_id):
    try:
        with get_connection() as conn:
            payment = conn.execute(
                """
                SELECT payment_id, amount, currency, status, created_at
                FROM payments
                WHERE payment_id = %s
                """,
                (payment_id,)
            ).fetchone()

        if payment is None:
            return jsonify({
                "error": "Payment ID not found",
                "payment_id": payment_id
            }), 404

        payment["amount"] = str(payment["amount"])
        payment["created_at"] = payment["created_at"].isoformat()
        return jsonify(payment), 200
    except Exception:
        return jsonify({"error": "Service temporarily unavailable"}), 503

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
