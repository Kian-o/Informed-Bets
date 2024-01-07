import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
api_key = 'YOUR_API_KEY'

response = requests.get(url=f"https://api.the-odds-api.com/v4/sports?apiKey={api_key}")
json_file_path = response.json()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('DELETE FROM sports_list')

for entry in json_file_path:
    cursor.execute('''
        INSERT INTO sports_list (sport, region_group, title, description, active, has_outrights)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entry['key'], entry['group'], entry['title'], entry['description'], entry['active'], entry['has_outrights']))

conn.commit()
conn.close()

