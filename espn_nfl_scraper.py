import json
import time  #https://www.geeksforgeeks.org/python/python-time-module/
import requests #https://www.w3schools.com/python/module_requests.asp
import mysql.connector #https://www.w3schools.com/python/python_mysql_getstarted.asp
from mysql.connector import errorcode #https://dev.mysql.com/doc/connector-python/en/connector-python-api-errorcode.html
from tqdm import tqdm #progress bar for scraping data(it takes a while)

#I have created a local sql database nfl_db so I will link to the database here

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*********",
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
        INSERT INTO Teams (team_id, abbrev, name, city, logo)
        VALUES (%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            abbrev=VALUES(abbrev),
            name=VALUES(name),
            city=VALUES(city),
            logo=VALUES(logo)
    """, (team["team_id"], team["abbrev"], team["name"], team["city"], team["logo"]))

conn.commit()  # save changes
conn.close()