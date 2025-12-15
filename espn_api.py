import requests

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

REGULAR_SEASON_WEEKS = 18
PLAYOFF_WEEKS = 5

def fetch_scoreboard(season, week, season_type):
    #order of params matters!!
    params = {
        "seasontype": season_type,
        "week": week,
        "year": season
    }
    resp = requests.get(SCOREBOARD_URL, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()

def fetch_full_season(season):
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        yield fetch_scoreboard(season, week, 2)

    for week in range(1, PLAYOFF_WEEKS + 1):
        yield fetch_scoreboard(season, week, 3)
