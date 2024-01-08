import os
import sqlite3

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for probability results
create_table_query = '''
CREATE TABLE IF NOT EXISTS probability (
    game_id            TEXT    PRIMARY KEY,
    bookmaker_id       INTEGER ,
    probability        INTEGER ,
    odds               INTEGER ,
    bookmaker_title    TEXT    ,
    market_key         TEXT    ,
    outcome_name       TEXT    ,
    last_update        TEXT    ,
    market_last_update TEXT    ,
    home_team          TEXT    ,
    away_team          TEXT    ,
    FOREIGN KEY (game_id) REFERENCES game_odds_staging(id)
);
'''
cursor.execute(create_table_query)
cursor.execute('DELETE FROM probability')
conn.commit()

# Insert results into probability table
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
    bookmakers_staging bmr
JOIN
    game_odds_staging gos ON bmr.game_id = gos.id
ORDER BY
    last_update DESC;
''')
cursor.execute(query)

conn.commit()

cursor.close()
conn.close()