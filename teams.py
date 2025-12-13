import json
from db import get_connection, execute

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