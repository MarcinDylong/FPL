# Fantasy Premier League Helper 

Fantasy Premier League Helper is a Django based app for optimizing user Team in Fantasy Premier League game using data from official game API. To learn more about game itself please find a link in Links section.
<br/>

## Key Notes
- App build in App Datta Able- Django Dashboard (link below);
- PostgreSQL Database, Django Native ORM
- Data from FPL API (end points below);
- Session-Based Authentication, Forms validation
- Deployment scripts: Docker;

<br/>


## How to use it

```bash
$ # Get the code
$ git clone https://github.com/MarcinDylong/FPL.git
$ cd FPL
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # Create in PostgreSQl database called fpl_data
$ sudo -u postgres psql -c 'create database fpl_data;'
$
$ # Configure connection to database in .env.example
$ # Provide username and password
$ # Remove .example from file name
$ # Also set SECRET_KEY you can use page below to generate your own secret key
$ # https://djecrety.ir/
$ # If necessary change parameters for DB connection in core/settings_local.py
$
$ # Create tables
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$
$ # Import data from fpl_dump.sql
$ fpl_data < fpl_dump_tables_updated.sql
$
$ # Start the application
$ python3 manage.py runserver --settings core.local_settings
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```
> Note: To use the app, you have to create user. After authentication, the app will be ready to use.
For using tools for data management like e.g. download Data from API, You have to create superuser:
```
$ # Create Super User
$ python manage.py createsuperuser
$ # Follow instructions in terminal to create Super User
```

## Deployment in Docker

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/)

### Docker execution


The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone https://github.com/MarcinDylong/FPL.git
$ cd FPL
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

> Populate database of project
```
$ sudo docker-compose exec web python manage.py migrate
$ sudo docker-compose exec web python manage.py createsuperuser
$ cat fpl_dump_tables_updated.sql | sudo docker exec -i fpl_db_1 psql -U postgres fpl_data
```

Alternatively, the data can be downloaded to database inside the application. After logging in as
Super User it is possible to use form to download all necessary data, but it takes longer than load
from fpl_dump_tables_updated.sql.

Visit `http://localhost:8000` in your browser. The app should be up & running.<br/>
You can use created Super User or create new user in App

## Heroku

For a quick preview, you can visit page:

https://fpl-helper.herokuapp.com/

This demo version has created Test user which allow to log in to application.

#### Important
Heroku version of application due to database size limitations contains gap in data!<br>
This means that some features or pages may be unavailable or there may be missing data in the tables.

## API endpoints used in project to download data:

Teams & players season data:
```
https://fantasy.premierleague.com/api/bootstrap-static/
```
Specific player data:
```
https://fantasy.premierleague.com/api/element-summary/{player_id}/
```
Season fixtures:
```
https://fantasy.premierleague.com/api/fixtures/
```
User data:
```
https://fantasy.premierleague.com/api/entry/{user_id}/
```
User team for given Game Week:
```
https://fantasy.premierleague.com/api/entry/{user_id}/event/{gw}/picks/
```

## Development:
- Providing more data from different sources to help better pick squad;
- Better data visualization;
- Implementing the ML algorithms for players data;
- Improvement in User Team View for better user experience;
- Bug Fixes;

## Credits & Links

### [Fantasy Premier League](https://fantasy.premierleague.com/)

Official page of Fantasy Premier League 


### [Django Dashboard - DattaAble Design](https://appseed.us/admin-dashboards/django-dashboard-dattaable)

Datta Able Bootstrap Lite is the most stylised Bootstrap 4 Lite Admin Template, around all other Lite/Free admin templates in the market. It comes with high feature-rich pages and components with fully developer-centric code. Before developing Datta Able our key points were performance and design.
