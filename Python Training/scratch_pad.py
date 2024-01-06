import json

json_file_path = "/Users/michaeloreilly/Documents/sports.json"

with open(json_file_path, 'r') as file:
    data = json.load(file)

print(data)