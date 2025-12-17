CREATE TABLE stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,   -- auto-incrementing unique ID
    game_id INTEGER NOT NULL,                    -- bigint → INTEGER
    team_id INTEGER NOT NULL,                    -- int → INTEGER
    win INTEGER NOT NULL,                        -- tinyint → INTEGER (0/1)
    first_downs INTEGER,                         -- nullable
    total_plays INTEGER,
    total_yards INTEGER,
    ypp REAL,                                    -- float → REAL
    tot_pass_yards INTEGER,
    interceptions INTEGER,
    sacks INTEGER,
    tot_rush_yards INTEGER,
    third_down_conversions INTEGER,
    third_down_attempts INTEGER,
    fourth_down_conversions INTEGER,
    fourth_down_attempts INTEGER,
    redzone_conversions INTEGER,
    redzone_attempts INTEGER,
    penalties INTEGER,
    fumbles INTEGER,
    time_poss_seconds INTEGER,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);