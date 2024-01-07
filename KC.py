import os
import sqlite3
import requests

bankroll = 10
fractional_kelly = 0.5  # Adjust this fraction as needed
db_path = os.path.expanduser("~/Documents/Kelly Criterion.sqlite")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for Kelly Criterion results
create_table_query = '''
CREATE TABLE IF NOT EXISTS kelly_criterion_results (
    game_id INTEGER PRIMARY KEY,
    bookmaker_id INTEGER,
    odds REAL,
    probability REAL,
    recommended_wager REAL
);
'''
cursor.execute(create_table_query)

# Commit the changes to the database
conn.commit()


# Function to calculate Kelly Criterion
def kelly_criterion(bankroll, odds, probability):
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
    recommended_wager = kelly_criterion(bankroll, odds, probability)

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
