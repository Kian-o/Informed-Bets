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

# Check if the response is a list
if isinstance(json_data, list):
    for data in json_data:
        # Insert game information into game_odds table
        cursor.execute('''
            INSERT INTO game_odds (id, sport_key, sport_title, commence_time, home_team, away_team)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['id'],
            data['sport_key'],
            data['sport_title'],
            data['commence_time'],
            data['home_team'],
            data['away_team']
        ))

        # Insert bookmaker information into bookmakers table
        for bookmaker in data['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    cursor.execute('''
                        INSERT INTO bookmakers (game_id, bookmaker_key, bookmaker_title, last_update, market_key, market_last_update, outcome_name, outcome_price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        data['id'],
                        bookmaker['key'],
                        bookmaker['title'],
                        bookmaker['last_update'],
                        market['key'],
                        market['last_update'],
                        outcome['name'],
                        outcome['price'],
                    ))

# Commit changes to the database
conn.commit()

# Close the connection
conn.close()