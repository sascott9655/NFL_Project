from db import get_connection, execute
from db_helpers import get_season_id, get_week_id, get_team_id
from espn_api import fetch_full_season
from abbrev_map import normalize_abbrev
from datetime import datetime

def insert_games(conn, games): #games is the parsed JSON response from scoreboard api endpoint
    if not games.get('events'): #deals with teams on a bye week
        return 
    
    for game in games['events']: #for each football game in the api
        game_id = int(game['id']) #retrieve the espn game id 
        espn_date = game['date'] #an ISO 8601 does not automatically convert to DATETIME in our database
        game_date = datetime.strptime(espn_date, "%Y-%m-%dT%H:%MZ")

        #variables that are retreiving espn api information
        season_year = game['season']['year']
        season_type = game['season']['type'] # 2 regular 3 playoffs
        week_number = game['week']['number']

        #making sure season_id and week_id keys align in the Seasons and Weeks tables
        season_id = get_season_id(conn, season_year)
        week_id = get_week_id(conn, season_id, season_type, week_number)

        competition = game['competitions'][0] # main competition object for the game (scores, teams, status)
        status = competition['status']['type']['name'] #status of game

        #determining which of two teams is the home team
        home = away = None
        
        for c in competition['competitors']:
            if c['homeAway'] == 'home':
                home = c
            elif c['homeAway'] == "away":
                away = c

        if not home or not away: #in case there is a game with no competitors
            continue

        #Calling our normalize abbrev function to check if teams have 
        #different mapping from the databases. If they do the abbreviation
        #should convert to the one in the database and therefore are able to
        #retrieve the appropriate team_id for the game

        home_abbrev = normalize_abbrev(home['team']['abbreviation'])
        away_abbrev = normalize_abbrev(away['team']['abbreviation'])

        invalid_abbrev = ["TBD", "AFC", "NFC"]

        #in keyword is like contains. (e.g) Does home_abbrev contain TBD OR AFC OR NFC?
        if home_abbrev in invalid_abbrev or away_abbrev in invalid_abbrev:
            continue

        home_team_id = get_team_id(conn, home_abbrev)
        away_team_id = get_team_id(conn, away_abbrev)

        #the if and else statement after getting the score is used during 
        #a live game so it wont crash if no score exist yet and if the scores
        #need to update they can
        home_score = int(home['score']) if home.get('score') is not None else None
        away_score = int(away['score']) if away.get('score') is not None else None

        execute(conn, """
                INSERT INTO Games (
                game_id, week_id, season_id,
                home_team_id, away_team_id,
                home_score, away_score,
                game_date, status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    home_score=VALUES(home_score),
                    away_score=VALUES(away_score),
                    status=VALUES(status)
                """, (
                    game_id, week_id, season_id, home_team_id,
                    away_team_id, home_score, away_score,
                    game_date, status
                ))
        
def run(season):
    conn = get_connection()
    for week_data in fetch_full_season(season):
        insert_games(conn, week_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run(2025)