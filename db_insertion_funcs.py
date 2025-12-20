from db import get_connection , execute, fetchone
from db_helpers import get_season_id
import json

REGULAR_SEASON_WEEKS = 18
PLAYOFF_WEEKS = 5

def insert_seasons(year):
    conn = get_connection()

    sql = '''
        INSERT INTO seasons (year)
        VALUES (%s)
        ON CONFLICT (year) DO NOTHING
    '''

    execute(conn, sql, (year,))
    conn.commit()
    conn.close()

insert_seasons(2025)


def insert_weeks(year):
    conn = get_connection()
    season_id = get_season_id(conn, year)

    sql = """
        INSERT INTO weeks (season_id,
        season_type, week_number)
        VALUES (%s, %s, %s)
        ON CONFLICT (season_id, season_type, week_number)
        DO NOTHING
    """

    #Regular season
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        execute(conn, sql, (season_id, 2, week))

    #Playoffs
    for week in range(1, PLAYOFF_WEEKS + 1):
        execute(conn, sql, (season_id, 3, week))

    conn.commit()
    conn.close()
    
insert_weeks(2025)


def insert_teams():
    with open("teams.json") as f:
        teams = json.load(f)

    conn = get_connection()

    for team in teams:
        execute(conn, """
                INSERT INTO teams (team_id, abbrev, name,
                city, logo, conference, division)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO UPDATE SET 
                abbrev = EXCLUDED.abbrev,
                name = EXCLUDED.name,
                city = EXCLUDED.city,
                logo = EXCLUDED.logo,
                conference = EXCLUDED.conference,
                division = EXCLUDED.division
                """,
                (team["team_id"],
                 team["abbrev"],
                 team["name"], 
                 team["city"],
                 team["logo"], 
                 team['conference'],
                 team['division']))
    
    conn.commit()
    conn.close()

insert_teams()