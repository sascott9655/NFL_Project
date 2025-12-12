import json
import mysql.connector #https://www.w3schools.com/python/python_mysql_getstarted.asp

#I have created a local sql database nfl_db so I will link to the database here
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="********",
    database="nfl_db"
)

with open("teams.json") as f:
    teams = json.load(f)


def execute(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()  
    cur.close()


for team in teams:
    execute(conn, """
        INSERT INTO Teams (team_id, abbrev, name, city, conference, division, logo)
        VALUES (%s,%s,%s,%s,%s,%s, %s)
        ON DUPLICATE KEY UPDATE
            abbrev=VALUES(abbrev),
            name=VALUES(name),
            city=VALUES(city),
            conference=VALUES(conference),
            division=VALUES(division),
            logo=VALUES(logo)
    """, (team["team_id"], team["abbrev"], team["name"], team["city"], team["conference"], team["division"], team["logo"]))

conn.commit()  # save changes
conn.close()






