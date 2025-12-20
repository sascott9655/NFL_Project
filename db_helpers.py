from db import fetchone

def get_season_id(conn, year):
    row = fetchone(
        conn,
        "SELECT season_id FROM seasons WHERE year=%s",
        (year,)
    )
    if row is None:
        raise ValueError(f"Season {year} not found")
    return row[0] #extracting integer value since returning row would return a tuple without indexing the tuple

def get_week_id(conn, season_id, season_type, week_number):
    row = fetchone(
        conn,
        """
        SELECT week_id
        FROM weeks
        WHERE season_id=%s AND season_type=%s AND week_number=%s
        """,
        (season_id, season_type, week_number)
    )
    if row is None:
        raise ValueError(f"Week values {(season_id, season_type, week_number)} not found")
    return row[0]

def get_team_id(conn, abbrev):
    row = fetchone(
        conn,
        "SELECT team_id FROM teams WHERE abbrev=%s",
        (abbrev,)
    )
    if row is None:
        raise ValueError(f"Team id {abbrev} not found")
    return row[0]