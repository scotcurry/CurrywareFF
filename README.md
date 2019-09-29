[Documentation on Writing and Formatting README.md](https://help.github.com/en/articles/basic-writing-and-formatting-syntax)

# Pseudo Documentation

## Django Server Information

- You build out models in the models.py file.  These become the tables in the SQL Lite database.  Whenever changes are made
you must run the command phython manage.py makemigrations, then phython manage.py migrate.  [List of Djange commands](https://docs.djangoproject.com/en/2.2/ref/django-admin/)

- **Note** After you create the App in the first step, there is a part that is missing that will make it so views won't render correctly.  You need to go to the _settings.py_ file in the main project and add the app name like the following:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    **'stats'**,
]

- If there is a problem with Cross Site errors you need to run the command: **python3 manage.py clearsessions**

## OAuth Information

## Yahoo API Information

Endpoint to get the game ID: https://fantasysports.yahooapis.com/fantasy/v2/game/nfl
Documentation link for the API:  https://developer.yahoo.com/fantasysports/guide/league-resource.html

Finding the game ID (value for that years NFL FF) is in the yahoo_ff_helper.py file get_game_id method, it is also currently stored in the YAML file.

league_id: 877754

All calls for league information use the format (for the 2019 year): league/390.l.877754
Exact endpoint for this year. https://fantasysports.yahooapis.com/fantasy/v2/league/390.l.877754