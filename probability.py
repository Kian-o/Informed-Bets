import os
import sqlite3

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = ('''INSERT OR REPLACE INTO probability (
    game_id,
    bookmaker_id,
    probability,
    odds,
    bookmaker_title,
    market_key,
    outcome_name,
    last_update,
    market_last_update,
    home_team,
    away_team
)
SELECT
    bmr.game_id,
    bmr.id as bookmaker_id,
    bmr.outcome_price / (bmr.outcome_price + 100) * 100 as probability,
    bmr.outcome_price as odds,
    bmr.bookmaker_title,
    bmr.market_key,
    bmr.outcome_name,
    bmr.last_update,
    bmr.market_last_update,
    gos.home_team,
    gos.away_team
FROM
    bookmakers bmr
JOIN
    game_odds gos ON bmr.game_id = gos.id
ORDER BY
    last_update DESC;
''')
cursor.execute(query)

conn.commit()

cursor.close()
conn.close()