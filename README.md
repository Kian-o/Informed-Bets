# Informed Bets

**Informed Bets** is a program designed to intelligently organize betting markets by leveraging the Kelly Criterion and bookmaker data.

## Overview

This program utilizes a locally saved SQLite3 database, connecting via [Ducklet](https://apps.apple.com/us/app/ducklet/id6447237898?mt=12) (available on the App Store) and [Python](https://www.python.org/downloads/).

## Kelly Criterion

Informed Bets employs the [Kelly Criterion](https://www.techopedia.com/gambling-guides/kelly-criterion-gambling) to assess odds and probabilities sourced from bookmakers worldwide.

## Data Source

Data for the program is sourced from [the-odds-api](https://the-odds-api.com), which offers various access plans. A free subscription allows for 500 requests per month.

**Run Order:**

1. sports_list_api.py
2. odds_api.py
3. probability.py
4. KC.py

**SQL for Results**

```sql
select 
kcr.*
, bms.* 

from kelly_criterion_results kcr

join bookmakers_staging bms
on kcr.bookmaker_id = bms.id


```

# Gambling Disclaimer

This website/application provides information and resources related to gambling, including odds, probabilities, and betting strategies. It is important to note that gambling involves risk, and individuals should exercise caution and responsible judgment when participating in any form of betting or gaming activities.

## Disclaimer:

- **Risk of Loss:** Gambling inherently carries the risk of financial loss. Participants should be aware that they may lose money, and it is advisable to only wager what one can afford to lose.

- **Legal Compliance:** Users are responsible for ensuring that their participation in gambling activities complies with the laws and regulations of their jurisdiction. The availability of certain games and betting options may vary based on local laws.

- **Responsible Gambling:** It is essential to gamble responsibly. If you believe you have a gambling problem or are experiencing negative consequences related to your gambling activities, seek assistance from relevant support organizations.

- **Age Restriction:** Users must be of legal age to engage in gambling activities in their jurisdiction. Minors are strictly prohibited from participating.

- **Accuracy of Information:** While efforts are made to provide accurate and up-to-date information, the website/application makes no warranties or representations regarding the correctness, completeness, or reliability of the content. Users are encouraged to verify information independently.

By using this website/application, you acknowledge and accept these terms. If you do not agree with these terms or are uncomfortable with the risks associated with gambling, it is advised to refrain from participating in any gambling activities.

*This disclaimer is subject to change without notice. Users are encouraged to review the disclaimer periodically for updates.*
