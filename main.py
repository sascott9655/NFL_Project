from db import get_connection, fetchall
from espn_api import fetch_reg_season
from games import insert_games
from team_stats import insert_team_stats


def connector(season):
    conn = get_connection()
    for week_json in fetch_reg_season(season):
        insert_games(conn, week_json) 

    games = fetchall(
    conn,
    """
    SELECT game_id
    FROM games
    WHERE status = 'STATUS_FINAL'
    """
    )

    for (game_id,) in games:
        insert_team_stats(conn, {"game_id": game_id})

    conn.commit()
    conn.close()

if __name__ == "__main__":
    connector(2025)