## FPL


### About:

Django based project to help improve your Team in Fantasy Premier League official game
using data downloaded from PL API: 

..* [https://fantasy.premierleague.com/api/bootstrap-static/]

### How to start:

..* Clone or download repository;
..* Configure connection with Database in PSQL;
..* Install required Python packages
..* Create Super User _( python3 manage.py createsuperuser )_;
..* Make migrations;
..* Runserver and log in as super user;
..* To populate from prepared JSON file in repository as super user
... respectively go through URL:
  1. /populate_teams/
  2. /populate_positions/
  3. /populate_players/
  
In order to populate database directly from Premier League API swap commentary:
```python
data = read_json() ## Read data from JSON file on disk
# data = get_data() ## Read data from JSON file from Fantasy Premier League API
```
In PopulateTeamsView, PopulatePositionsView and PopulatePlayersView.







