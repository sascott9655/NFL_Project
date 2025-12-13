from db import get_connection, execute, fetchone
from seasons import get_season_id

#game amount
REGULAR_SEASON_WEEKS = 18 
PLAYOFF_WEEKS = 5 

def insert_weeks(year):
    season_id = get_season_id(year)
    conn = get_connection()

    sql = """
    INSERT INTO Weeks (season_id, season_type, week_number)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE week_number = week_number    
    """

    #Regular season
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        execute(conn, sql, (season_id, 2, week))

    #Playoffs
    for week in range(1, PLAYOFF_WEEKS + 1):
        execute(conn,sql, (season_id, 3, week))

    conn.commit()
    conn.close()

insert_weeks(2025)

