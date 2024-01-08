import os
import sqlite3
from Functions_combined import update_sports_list, update_game_odds, calculate_and_update_kelly_criterion

# Example usage
api_key = '0fd2e16c8b08df43c7c557f0384da54a'
db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")
sport = 'americanfootball_nfl'
bankroll = 10
fractional_kelly = 0.5

update_sports_list(api_key, db_path)
update_game_odds(api_key, sport, db_path)
calculate_and_update_kelly_criterion(bankroll, fractional_kelly, db_path)
