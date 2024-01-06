import os
import sqlite3
import json

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
json_file_path = "/Users/michaeloreilly/Documents/sports.json"

with open(json_file_path, 'r') as file:
    data = json.load(file)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


for entry in data:
    cursor.execute('''
        INSERT INTO sports_list (sport, region_group, title, description, active, has_outrights)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entry['key'], entry['group'], entry['title'], entry['description'], entry['active'], entry['has_outrights']))

conn.commit()
conn.close()

