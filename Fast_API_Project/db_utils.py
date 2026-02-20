import os
import traceback

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    """Create and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except psycopg2.Error as exc:
        raise RuntimeError(f"PostgreSQL connection failed: {exc}") from exc


def add_log_entry(level, message):
    """Add a log entry to the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO logs (level, message) VALUES (%s, %s)",
                (level, message),
            )
            conn.commit()
    except Exception as exc:
        print(f"Error adding log entry: {exc}")
    finally:
        conn.close()


def save_error_log(error_obj, endpoint_name):
    full_traceback = traceback.format_exc()
    error_type = type(error_obj).__name__
    message = str(error_obj)

    sql = """
        INSERT INTO error_logs (error_type, message, traceback, endpoint)
        VALUES (%s, %s, %s, %s)
    """
    params = [error_type, message, full_traceback, endpoint_name]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()
    except Exception as exc:
        print(f"Error saving error log: {exc}")
    finally:
        conn.close()


def save_request_to_db(data):
    sql = """
        INSERT INTO request_logs (method, path, ip_address, status_code, duration_ms)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = [data["method"], data["path"], data["ip"], data["status"], data["duration"]]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            conn.commit()
    except Exception as exc:
        print(f"Logging failed: {exc}")
    finally:
        conn.close()
