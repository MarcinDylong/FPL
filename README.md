# Fantasy Premier League Helper 

Fantasy Premier League Helper is a Django based app for optimizing user Team in Fantasy Premier League game using data from official game API. To learn more about game itself please find a link in Links section.
<br/>

## Key Notes
- App build in App Datta Able- Django Dashboard (link below);
- PostgreSQL Database, Django Native ORM
- Data from FPL API (end points below);
- Session-Based Authentication, Forms validation
- Deployment scripts: Docker;

<br />


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
$ # Configure connection to database in _secrets.json
$ # Provide username and password and remove "_" from json file name
$ # If necessary change parameters for DB connection in core/settings_local.py
$
$ # Create tables
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$
$ # Create in PostgreSQl database called fpl_data
$ sudo -u postgres psql -c 'create database fpl_data;'
$ # Import data from fpl_dump.sql
$ pg_restore -d fpl_data < fpl_dump.sql
$
$ # Start the application
$ python3 manage.py runserver --settings core.settings_local
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```
> Note: To use the app, please access the registration page and **create a new user**. After authentication, the app will unlock the private pages.
For using tools for data management like download Data from API You have to create superuser:
```
$ # Create Super User
$ python manage.py createsuperuser
$ # Follow instructions in terminal to create Super User
```
You may also use User from loaded database; <br>
Data for log in: <br>
User: admin <br>
Pass: admin
<br/>

## Deployment in Docker

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/)

### Docker execution


The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone https://github.com/app-generator/django-dashboard-dattaable.git
$ cd django-dashboard-dattaable
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

> Populate database of project
```
$ sudo docker exec -i -u postgres fpl_db_1 pg_restore -d fpl_data < fpl_dump.sql
$ sudo docker-compose exec web python manage.py migrate
```

Visit `http://localhost:8000` in your browser. The app should be up & running.<br/>
Note: You may use User from database and log in as:<br/>
Username: admin<br/>
password: admin

## API endpoints used in project

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
