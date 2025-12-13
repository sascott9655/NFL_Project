import json
import mysql.connector #https://www.w3schools.com/python/python_mysql_getstarted.asp

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!Woody1013!",
        database="nfl_db"
    )

def execute(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    cur.close()

def fetchone(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    r = cur.fetchone()
    cur.close()
    return r

def fetchall(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    r = cur.fetchall()
    cur.close()
    return r
