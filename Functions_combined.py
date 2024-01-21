import os
import sqlite3
import requests


# Functions included:
# update_sports_list(api_key, db_path)
# update_game_odds(api_key, sport, db_path)
# calculate_and_update_kelly_criterion(bankroll, fractional_kelly, db_path)

def update_sports_list(api_key, db_path):
    response = requests.get(url=f"https://api.the-odds-api.com/v4/sports?apiKey={api_key}")
    json_file_path = response.json()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table for sports_list results
    create_sports_list_staging_query = '''
    CREATE TABLE IF NOT EXISTS sports_list_staging (
        sport         TEXT PRIMARY KEY,
        region_group  TEXT ,
        title         TEXT ,
        description   TEXT ,
        active        TEXT ,
        has_outrights TEXT
    );
    '''
    cursor.execute(create_sports_list_staging_query)
    conn.commit()

    cursor.execute('DELETE FROM sports_list_staging')

    # Insert sports list results into sports_list table
    for entry in json_file_path:
        cursor.execute('''
            INSERT INTO sports_list_staging (sport, region_group, title, description, active, has_outrights)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            entry['key'], entry['group'], entry['title'], entry['description'], entry['active'],
            entry['has_outrights']))

    conn.commit()
    conn.close()


# Example usage
api_key = 'YOUR_API_KEY'
db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

update_sports_list(api_key, db_path)


def update_game_odds(api_key, sport, db_path):
    # Make API request
    response = requests.get(
        url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds?apiKey={api_key}&regions=us&oddsFormat=american")
    json_data = response.json()

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table for Game Odds results
    create_game_odds_staging_query = '''
    CREATE TABLE IF NOT EXISTS game_odds_staging (
        id            TEXT PRIMARY KEY,
        sport_key     TEXT ,
        sport_title   TEXT ,
        commence_time TEXT ,
        home_team     TEXT ,
        away_team     TEXT 
    );
    '''
    # Create a table for Bookmaker results
    create_bookmakers_staging_query = '''
    CREATE TABLE IF NOT EXISTS bookmakers_staging (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id             TEXT    ,
        bookmaker_key       TEXT    ,
        bookmaker_title     TEXT    ,
        last_update         TEXT    ,
        market_key          TEXT    ,
        market_last_update  TEXT    ,
        outcome_name        TEXT    ,
        outcome_price       INTEGER ,
        outcome_description TEXT    ,
        outcome_point       INTEGER ,
        FOREIGN KEY (game_id) REFERENCES game_odds_staging(id)
    );
    '''
    cursor.execute(create_game_odds_staging_query)
    cursor.execute(create_bookmakers_staging_query)
    cursor.execute('DELETE FROM game_odds_staging')
    cursor.execute('DELETE FROM bookmakers_staging')
    conn.commit()

    # Insert game information into game_odds table
    if isinstance(json_data, list):
        for data in json_data:
            cursor.execute('''
                INSERT INTO game_odds_staging (id, sport_key, sport_title, commence_time, home_team, away_team)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['id'],
                data['sport_key'],
                data['sport_title'],
                data['commence_time'],
                data['home_team'],
                data['away_team']
            ))

    # Insert bookmaker information into bookmakers table
    for item in json_data:
        for bookmaker in item['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    cursor.execute('''
                        INSERT INTO bookmakers_staging (game_id, bookmaker_key, bookmaker_title, last_update, market_key, market_last_update, outcome_name, outcome_price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item['id'],
                        bookmaker['key'],
                        bookmaker['title'],
                        bookmaker['last_update'],
                        market['key'],
                        market['last_update'],
                        outcome['name'],
                        outcome['price'],
                    ))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Example usage

sport = 'americanfootball_nfl'

update_game_odds(api_key, sport, db_path)


def calculate_and_update_kelly_criterion(bankroll, fractional_kelly, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table for Kelly Criterion results
    create_kelly_criterion_results_query = '''
    CREATE TABLE IF NOT EXISTS kelly_criterion_results (
        game_id INTEGER PRIMARY KEY,
        bookmaker_id INTEGER,
        odds REAL,
        probability REAL,
        recommended_wager REAL
    );
    '''
    cursor.execute('DELETE FROM kelly_criterion_results')
    cursor.execute(create_kelly_criterion_results_query)

    # Commit the changes to the database
    conn.commit()

    # Function to calculate Kelly Criterion
    def kelly_criterion(odds, probability):
        b = odds - 1  # Convert odds to decimal form
        p = probability
        q = 1 - p
        bp = b * p
        f_star = (bp - q) / b
        return fractional_kelly * f_star * bankroll  # Use a fraction of the calculated Kelly fraction

    # Query to fetch odds, probability, game_id, and bookmaker_id from the 'probability' table
    query = "SELECT game_id, bookmaker_id, odds, probability FROM probability"
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # Process and insert Kelly Criterion results into the new table
    for row in results:
        game_id, bookmaker_id, odds, probability = row
        recommended_wager = kelly_criterion(odds, probability)

        # Insert results into kelly_criterion_results table
        insert_query = '''
        INSERT OR REPLACE INTO kelly_criterion_results (game_id, bookmaker_id, odds, probability, recommended_wager)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_query, (game_id, bookmaker_id, odds, probability, recommended_wager))

    # Commit the changes to the database
    conn.commit()

    # Print the results (optional)
    cursor.execute("SELECT * FROM kelly_criterion_results")
    kelly_results = cursor.fetchall()
    for result in kelly_results:
        print(
            f"Game ID: {result[0]}, Bookmaker ID: {result[1]}, Odds: {result[2]}, Probability: {result[3]}, Recommended Wager: {result[4]:.2f} units of your bankroll")

    # Close the cursor and connection
    cursor.close()
    conn.close()


# Example usage
bankroll = 10
fractional_kelly = 0.5  # Adjust this fraction as needed

calculate_and_update_kelly_criterion(bankroll, fractional_kelly, db_path)
