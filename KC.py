# Kelly Criterion for Gambling

# F* = p - (q/b) = p - ((1-p)/b)

# F* - fraction of current bankroll to wager
# p - probability of a win
# q - probability of a loss (q=1-p)
# b - proportion of the bet gained with a win
#Changes


# Top level api: The Odds API

import os
import sqlite3
import requests

db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sport = 'americanfootball_nfl'

api_key = '0fd2e16c8b08df43c7c557f0384da54a'

response = requests.get(url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds?apiKey={api_key}&regions=us&oddsFormat=american")

data = response.json()

print(data)