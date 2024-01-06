import requests

response = requests.get(url="https://api.the-odds-api.com/v4/sports?apiKey=0fd2e16c8b08df43c7c557f0384da54a")

data = response.json()

print(data)
