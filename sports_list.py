import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

response = requests.get(url="https://api.the-odds-api.com/v4/sports?apiKey=0fd2e16c8b08df43c7c557f0384da54a")
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

