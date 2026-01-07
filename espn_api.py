import requests

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

REGULAR_SEASON_WEEKS = 18
PLAYOFF_WEEKS = 5

def fetch_games(season, week, season_type):
    #order of params matters!!
    params = {
        "seasontype": season_type,
        "week": week,
        "year": season
    }
    resp = requests.get(SCOREBOARD_URL, params=params, timeout=25)
    resp.raise_for_status()
    return resp.json()

def fetch_reg_season(season):
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        yield fetch_games(season, week, 2) # https://www.geeksforgeeks.org/python/python-yield-keyword/

#playoff games are not necessary 
    # for week in range(1, PLAYOFF_WEEKS + 1):
    #     yield fetch_scoreboard(season, week, 3)

GAME_SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary"

def fetch_team_stats(event_id):
    params = {
        "event": event_id
    }
    resp = requests.get(GAME_SUMMARY_URL, params=params, timeout=25)
    resp.raise_for_status()

    return resp.json()
