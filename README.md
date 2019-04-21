# NYCSubwaySurfer

This is a Django web app that was created to track the arrivals of NYC MTA subways on the 1, 2, 3, 4, 5, 6 subway lines.
API calls are made to the NYC MTA's transit feed and parsed to find the correct trains.  This web app features a simple
front end interface to display incoming trains as well as its own API to get JSON information of incoming trains.
Subway stations unique identifiers are provided by the MTA and imported into a SQLite database.

Usage:
======

To use this web app, run the importStops.py file using the built-in Python shell in Django to load all subway 
station stops' unique IDs from stop.csv.

In the subwaysurfer directory run:

python manage.py shell

exec(open('importStops.py').read())

API Keys:
========

To use this web app, a key from the MTA is necessary (can be found here: https://datamine.mta.info/feed-documentation)

Create a config.env file in the root directory of the app and enter them there with the API keys

DJANGO_SECRET_KEY = 

MTA_API_KEY =  

Requirements:
============

Required dependencies can be found in the requirements.txt file