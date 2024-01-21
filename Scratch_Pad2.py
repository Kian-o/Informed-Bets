import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sport = 'americanfootball_nfl'
api_key = '0fd2e16c8b08df43c7c557f0384da54a'
response = requests.get(url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds?markets=spreads&apiKey={api_key}&regions=us&oddsFormat=american")
json_data = response.json()

print(json_data)