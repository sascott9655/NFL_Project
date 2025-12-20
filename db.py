import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )

def execute(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())

def fetchone(conn, sql, params=None):
     with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()
    

def fetchall(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()
