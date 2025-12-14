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

def get_season_id(conn, year):
    row = fetchone(conn, "SELECT season_id FROM Seasons WHERE year=%s", (year,))
    return row[0]

def get_week_id(conn, season_id, season_type, week_number):
    row = fetchone(conn, '''
            SELECT week_id
            FROM Weeks
            WHERE season_id=%s AND season_type=%s AND week_number=%s
            ''', (season_id, season_type, week_number))
    return row[0]

def get_team_id(conn, abbrev):
    row = fetchone(conn, "SELECT team_id FROM Teams WHERE abbrev=%s", (abbrev,))
    return row[0]