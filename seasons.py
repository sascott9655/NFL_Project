from db import get_connection, fetchone

def get_season_id(year):
    conn = get_connection()
    row = fetchone(conn, "SELECT season_id FROM Seasons WHERE year = %s", (year,))
    conn.close()
    return row[0] #returns 2025
