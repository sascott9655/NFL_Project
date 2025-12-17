import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="$$$$$$$$$$$$$",
        database="nfl_db"
    )

def execute(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    cur.close()

def fetchone(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    row = cur.fetchone()
    cur.close()
    return row

def fetchall(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    return rows