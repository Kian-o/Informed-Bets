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
create_table_query = '''
CREATE TABLE IF NOT EXISTS game_odds (
    id            TEXT PRIMARY KEY,
    sport_key     TEXT ,
    sport_title   TEXT ,
    commence_time TEXT ,
    home_team     TEXT ,
    away_team     TEXT 
);
'''
cursor.execute(create_table_query)
conn.commit()

# Insert game information into game_odds table

cursor.execute('''
    INSERT INTO game_odds (id, sport_key, sport_title, commence_time, home_team, away_team)
    VALUES (?, ?, ?, ?, ?, ?)
''', (
    json_data['id'],
    json_data['sport_key'],
    json_data['sport_title'],
    json_data['commence_time'],
    json_data['home_team'],
    json_data['away_team']
))

# Commit changes to the database
conn.commit()

# Create a table for Bookmaker results
create_table_query = '''
CREATE TABLE IF NOT EXISTS bookmakers (
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
    FOREIGN KEY (game_id) REFERENCES game_odds(id)
);
'''
cursor.execute(create_table_query)
conn.commit()

# Insert bookmaker information into bookmakers table
for bookmaker in json_data['bookmakers']:
    for market in bookmaker['markets']:
        for outcome in market['outcomes']:
            cursor.execute('''
                INSERT INTO bookmakers (game_id, bookmaker_key, bookmaker_title, last_update, market_key, market_last_update, outcome_name, outcome_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                json_data['id'],
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
