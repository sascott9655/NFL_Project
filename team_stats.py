from db import execute, fetchone, get_connection
from db_helpers import get_team_id
from espn_api import fetch_team_stats
from abbrev_map import normalize_abbrev

#we are also transforming our stats so it is easier to say run a model to predict win outcomes
def insert_team_stats(conn, game_id):
    game_id = int(game_id)
    team_stats = fetch_team_stats(game_id) #obtain appropriate game id

    teams = team_stats['boxscore']['teams'] #get the teams from the boxscore

    for t in teams:
        abbrev = normalize_abbrev(t['team']['abbreviation']) #get abbreviations of teams
        team_id = get_team_id(conn, abbrev) #convert them to our database ids

        #dictionary comprehension: shorthand for showing all the stats from the api
        stats = {s['name']: s['displayValue'] for s in t['statistics']}
    
        td_made, td_att = parse_made_att(stats.get('thirdDownEff'))
        fd_made, fd_att = parse_made_att(stats.get('fourthDownEff'))
        rz_made, rz_att = parse_made_att(stats.get('redZoneAttempts'))

        

        #turns minutes and seconds string to flat out seconds ex: "25:08' turn into 1508
        time_poss_seconds = parse_time_possession(stats.get('possessionTime')) #parses out minutes and seconds from string 

        win = compute_win(conn, game_id, team_id)

        if win is None:
            return

        execute(conn, """
                INSERT INTO TeamStats (
                game_id, team_id, win,
                first_downs, total_plays, total_yards, ypp,
                tot_pass_yards, interceptions, sacks, tot_rush_yards,
                third_down_conversions, third_down_attempts, fourth_down_conversions, fourth_down_attempts,
                redzone_conversions, redzone_attempts, penalties, fumbles,
                time_poss_seconds)
                VALUES (%s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    win=VALUES(win),
                    first_downs=VALUES(first_downs),
                    total_plays=VALUES(total_plays),
                    total_yards=VALUES(total_yards),
                    ypp=VALUES(ypp),
                    tot_pass_yards=VALUES(tot_pass_yards),
                    interceptions=VALUES(interceptions),
                    sacks=VALUES(sacks),
                    tot_rush_yards=VALUES(tot_rush_yards),
                    third_down_conversions=VALUES(third_down_conversions),
                    third_down_attempts=VALUES(third_down_attempts),
                    fourth_down_conversions=VALUES(fourth_down_conversions),
                    fourth_down_attempts=VALUES(fourth_down_attempts),
                    redzone_conversions=VALUES(redzone_conversions),
                    redzone_attempts=VALUES(redzone_attempts),
                    penalties=VALUES(penalties),
                    fumbles=VALUES(fumbles),
                    time_poss_seconds=VALUES(time_poss_seconds)
                """, (
                    game_id, team_id, win, 
                    int(stats.get('firstDowns', 0)),
                    int(stats.get('totalOffensivePlays', 0)),
                    int(stats.get('totalYards', 0)),
                    float(stats.get('yardsPerPlay', 0)),
                    int(stats.get('netPassingYards', 0)),
                    int(stats.get('interceptions', 0)),
                    int(stats.get('sacks', 0)),
                    int(stats.get('rushingYards', 0)),
                    td_made, td_att,
                    fd_made, fd_att,
                    rz_made, rz_att,
                    int(stats.get('penalties', 0)),
                    int(stats.get('fumblesLost', 0)),
                    time_poss_seconds
                ))
        
def parse_made_att(value, default="0-0"):
    """
    Safely parse ESPN stat strings like '7-11'
    Returns (made, attempts) as ints
    """
    if not value or "-" not in value:
        return 0, 0
    made, att = value.split("-")
    return int(made), int(att)

def parse_time_possession(value):
    """
    Parse ESPN possession time 'MM:SS'
    Returns total seconds as int
    """
    if not value or ":" not in value:
        return 0

    minutes, seconds = value.split(":")
    return int(minutes) * 60 + int(seconds)
    
    

        
def compute_win(conn, game_id, team_id):
    row = fetchone(conn, """
            SELECT home_team_id, away_team_id, home_score, away_score
            FROM Games
            WHERE game_id = %s       
    """, (game_id,))

    #game_id is a tuple. So we need to separate it in order to get the scores of the game
    #to determine the winner. We break up the tuple like so:

    home_id, away_id, home_score, away_score = row
    #print(row)

    if home_score is None or away_score is None:
        return None #if game hasnt started yet
    
    if team_id == home_id: #set winning to be 1 which is win in binary
        return int(home_score > away_score) #if true then home team is set to 1. If not true home team is set to 0
    else:
        return int(away_score > home_score) #If away team wins set to 1

#conn = get_connection()

#print(compute_win(conn, 401772510, 26))
