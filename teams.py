import json
from db import get_connection, execute

conn = get_connection()

with open("teams.json") as f:
    teams = json.load(f)

for team in teams:
    execute(conn, """
        INSERT INTO Teams (team_id, abbrev, name, city, logo)
        VALUES (%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            abbrev=VALUES(abbrev),
            name=VALUES(name),
            city=VALUES(city),
            logo=VALUES(logo)
    """, (team["team_id"], team["abbrev"], team["name"], team["city"], team["logo"]))
    
conn.commit()
conn.close()