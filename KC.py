# Kelly Criterion for Gambling

# F* = p - (q/b) = p - ((1-p)/b)

# F* - fraction of current bankroll to wager
# p - probability of a win
# q - probability of a loss (q=1-p)
# b - proportion of the bet gained with a win
#Changes


# Top level api: The Odds API
import requests

response = requests.get(url="https://api.the-odds-api.com/v4/sports?apiKey=0fd2e16c8b08df43c7c557f0384da54a")

data = response.json()

print(data)