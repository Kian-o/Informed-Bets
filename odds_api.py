import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sport = 'americanfootball_nfl'
api_key = 'YOUR_API_KEY'
response = requests.get(url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds?apiKey={api_key}&regions=us&oddsFormat=american")
json_data = response.json()

# Create a table for Game Odds results
create_game_odds_staging_query = '''
CREATE TABLE IF NOT EXISTS game_odds_staging (
    id            TEXT PRIMARY KEY,
    sport_key     TEXT ,
    sport_title   TEXT ,
    commence_time TEXT ,
    home_team     TEXT ,
    away_team     TEXT 
);
'''
# Create a table for Bookmaker results
create_bookmakers_staging_query = '''
CREATE TABLE IF NOT EXISTS bookmakers_staging (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id             TEXT    ,
    bookmaker_key       TEXT    ,
    bookmaker_title     TEXT    ,
    last_update         TEXT    ,
    market_key          TEXT    ,
    market_last_update  TEXT    ,
    outcome_name        TEXT    ,
    outcome_price       INTEGER ,
    outcome_description text    ,
    outcome_point       integer ,
    FOREIGN KEY (game_id) REFERENCES game_odds_staging(id)
);
'''
cursor.execute(create_game_odds_staging_query)
cursor.execute(create_bookmakers_staging_query)
cursor.execute('DELETE FROM game_odds_staging')
cursor.execute('DELETE FROM bookmakers_staging')
conn.commit()

# Insert game information into game_odds table
# Check if the response is a list
if isinstance(json_data, list):
    for data in json_data:
        # Insert game information into game_odds table
        cursor.execute('''
            INSERT INTO game_odds_staging (id, sport_key, sport_title, commence_time, home_team, away_team)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['id'],
            data['sport_key'],
            data['sport_title'],
            data['commence_time'],
            data['home_team'],
            data['away_team']
        ))

# Commit changes to the database
conn.commit()

# Insert bookmaker information into bookmakers table
# Insert bookmaker information into bookmakers table
for item in json_data:
    for bookmaker in item['bookmakers']:
        for market in bookmaker['markets']:
            for outcome in market['outcomes']:
                cursor.execute('''
                    INSERT INTO bookmakers_staging (game_id, bookmaker_key, bookmaker_title, last_update, market_key, market_last_update, outcome_name, outcome_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['id'],
                    bookmaker['key'],
                    bookmaker['title'],
                    bookmaker['last_update'],
                    market['key'],
                    market['last_update'],
                    outcome['name'],
                    outcome['price'],
                ))

# Commit changes and close the connection
conn.commit()
conn.close()
