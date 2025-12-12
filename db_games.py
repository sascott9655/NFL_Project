#import a function that connects to db in db.py
from db import get_connection, execute, fetchone, fetchall
import requests #requests are calls for online apis like espn's
from pprint import pprint

# #function that inserts web scraped data in database (we havent web scraped yet)
# def insert_game(game):
#     conn = get_connection()
    
#     sql="""
#         INSERT INTO Games (
#             game_id, week_id, season_id, home_team_id, away_team_id,
#             home_score, away_score, game_date, status
#             )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         ON DUPLICATE KEY UPDATE
#             home_score=VALUES(home_score),
#             away_score=VALUES(away_score).
#             status = VALUES(status),
#             game_date = VALUES(game_date);
#         """
#     params = (
#         game['game_id'], # ex: "401772948"
#         game['week_id'], # ex: 1
#         game['season_id'], # ex: 2024
#         game['home_team_id'], #ex: 49ers
#         game['away_team_id'], #ex: Eagles
#         game['home_score'], # ex: 31
#         game['away_score'], # ex: 28
#         game['game_date'], #ex: 2024-09-07T20:25Z 
#         game['status'] #ex: Final
#     )

#     execute(sql, params)
#     conn.commit()
#     conn.close()

    #I want to link my own understanding and documentation via link
    #to show my learning and be able to explain to other people my
    #project. For now I will show it here.
    #Example of JSON output from ESPN scoreboard:

HEADERS = {
    "User-Agent": "nfl-scraper/1.0 (+https://yourdomain.example) Python/requests"
}

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

resp = requests.get(SCOREBOARD_URL, headers=HEADERS)
data = resp.json()

# Look at the first game
first_game = data["events"][0]
competitors = first_game["competitions"][0]["competitors"]

for team in competitors:
    pprint(team) #pretty print

    


    #When scraping from ESPN only team abbreviations will be used and 
    #not the team_id used in my database. Therefore it is necessary to
    #create a map and convert the ESPN abbreviations to the team_id
    #to read team information on game day

    # TEAM_MAP = {
    #     "":

    # }

    



