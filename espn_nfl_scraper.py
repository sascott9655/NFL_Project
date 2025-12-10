# credit to https://github.com/pseudo-r/Public-ESPN-API 
# section 5 for providing espn API

#using nfl env with python version 3.12
'''
Docstring for espn_nfl_scraper
Populates Teams, Seasons, Weeks, Games, TeamStats using 
ESPN hidden API endpoints
'''

import time  #https://www.geeksforgeeks.org/python/python-time-module/
import requests #https://www.w3schools.com/python/module_requests.asp
import mysql.connector #https://www.w3schools.com/python/python_mysql_getstarted.asp
from mysql.connector import errorcode #https://dev.mysql.com/doc/connector-python/en/connector-python-api-errorcode.html
from tqdm import tqdm #progress bar for scraping data(it takes a while)

#I have created a local sql database nfl_db so I will link to the database here

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "!Woody1013!", #need to properly encrypt password
    "database": "nfl_db",
}

#shows espn that I am not a robot scraping data. Using data for hobby purposes.
HEADERS = {
    "User-Agent": "nfl-scraper/1.0 (+https://yourdomain.example) Python/requests"
}

#season we are scraping
SEASONS = [2020, 2021, 2022, 2023, 2024, 2025]

#pause between requests to avoid hammering ESPN
REQUEST_SLEEP = 0.3

#espn endpoints from github
SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
TEAMS_LIST = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
BOXSCORE = "https://https://cdn.espn.com/core/nfl/boxscore"

# ========= DB HELPER FUNCTIONS ==========

def db_connect():
    return mysql.connector.connect(**DB_CONFIG)

def execute(conn, sql, params=None):
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

# =========== UTIL ==========
def safe_get(url, params=None, retries=3, backoff=1.0):
    attempt = 0
    while attempt < retries:
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if r.status_code == 200: # means success status code
                return r.json()
            else:
                print(f"HTTP {r.status_code} for {r.url}")
        except Exception as e:
            print("Request error:", e)
        attempt += 1
        time.sleep(backoff * attempt)
    return None

#understanding of safe_get -> it will extract the data needed from espn
#it will attempt to do so 3 times, if it is safe to do so it will return
#the data in json format. Otherwise it will tell you the status code error
#and it will increase the wait time of retrieving the data by backoff*attempts 


