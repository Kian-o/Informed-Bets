import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
api_key = 'YOUR_API_KEY'

response = requests.get(url=f"https://api.the-odds-api.com/v4/sports?apiKey={api_key}")
json_file_path = response.json()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for sports_list results
create_table_query = '''
CREATE TABLE IF NOT EXISTS sports_list (
    sport         TEXT PRIMARY KEY,
    region_group  TEXT ,
    title         TEXT ,
    description   TEXT ,
    active        TEXT ,
    has_outrights TEXT
);
'''
cursor.execute(create_table_query)
conn.commit()

cursor.execute('DELETE FROM sports_list')

# Insert sports list results into sports_list table
for entry in json_file_path:
    cursor.execute('''
        INSERT INTO sports_list (sport, region_group, title, description, active, has_outrights)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entry['key'], entry['group'], entry['title'], entry['description'], entry['active'], entry['has_outrights']))

conn.commit()
conn.close()
