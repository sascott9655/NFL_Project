SELECT * from games; #imported data from espn api about NFL games that happened this year
SELECT * from games ORDER BY week_id; #ordered by week_id instead of game_id
SELECT week_id, home_team_id, away_team_id, home_score, away_score FROM Games ORDER by week_id; #selected columns important for questions about the NFL dataset

# Do teams score more points at home or on the road?
SELECT AVG(g.home_score) AS avg_home_score, AVG(g.away_score) AS avg_away_score
FROM Games g
JOIN weeks w ON w.week_id = g.week_id
WHERE w.week_number <= 15; 
#Home team scores more on average by roughly 2 more points than away team. Playing at home gives teams a slight advantage in winning football games.

#What teams are scoring the most points? The least amount of points? lets get the whole list 
SELECT t.team_id, t.name, SUM(normalized_gp.points) AS total_points
FROM (    
SELECT home_team_id AS team_id, home_score AS points
FROM Games g


UNION ALL -- preserves all rows vs Union which removes duplicates

SELECT away_team_id AS team_id, away_score AS points
FROM Games g
) normalized_gp -- temporary table query
JOIN teams t ON t.team_id = normalized_gp.team_id -- how the points are gathered for one team then added up by the SUM function above
GROUP BY t.team_id, t.name
order by total_points DESC 
#The teams that are scoring the most points are playoff contenders teams. Scoring is how a football is won so scoring team probably correlates to team success.