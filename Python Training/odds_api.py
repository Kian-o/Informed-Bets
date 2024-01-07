import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sport = 'americanfootball_nfl'
api_key = '0fd2e16c8b08df43c7c557f0384da54a'
response = requests.get(url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds?apiKey={api_key}&regions=us&oddsFormat=american")
json_data = response.json()

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
