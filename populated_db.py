#populate database with this three functions no web scraping required
#populated season 2025, weeks 1-18 reg, postseason, and teams
#run this file only once to do so

import json
from helper_func_db import get_connection, fetchone, execute

def pop_season_id(conn, year):
    conn = get_connection()
    row = fetchone(conn, "SELECT season_id FROM Seasons WHERE year = %s", (year,))
    conn.close()
    return row[0] #returns 2025

#game amount
REGULAR_SEASON_WEEKS = 18 
PLAYOFF_WEEKS = 5 

def pop_weeks(year):
    season_id = pop_season_id(year)
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

pop_weeks(2025)


with open("teams.json") as f:
    teams = json.load(f)

conn = get_connection()

for team in teams:
    execute(conn, """
    INSERT INTO Teams (team_id, abbrev, name, city, logo)
    VALUES (%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
    abbrev=VALUES(abbrev),
    name=VALUES(name),
    city=VALUES(city),
    logo=VALUES(logo),
    conference=VALUES(conference),
    division=VALUES(division)  
    """, (team["team_id"], team["abbrev"], team["name"], team["city"], team["logo"], team['conference'], team['division']))


conn.commit()  # save changes
conn.close()