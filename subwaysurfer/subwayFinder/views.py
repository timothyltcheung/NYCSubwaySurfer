from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import StationStop
from google.transit import gtfs_realtime_pb2
import requests
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Import .env file with API keys

mta_api_key = os.environ['MTA_API_KEY']


def index(request):
    # use a set to grab unique values of station names, which could have multiple station codes associated
    uniqueStopNames = set([station.stopname for station in StationStop.objects.all()])
    context = {
        "stations": uniqueStopNames  # Pass in unique station names to populate dropdown
    }
    return render(request, "subwayFinder/index.html", context)


def arrival(request):
    # Get route, station, direction from POST request form submission
    route = request.POST["route"]
    station = request.POST["stationstops"]
    direction = request.POST["direction"]

    directiondict = {"S": "Southbound", "N": "Northbound"}

    # Each station can have multiple station codes
    # Grab station codes from imported database mapping station codes to stations with direction
    stations = StationStop.objects.all().filter(stopname=station)
    stationCodes = [x.stopcode + direction for x in stations]

    # Make request to MTA GFTS API
    currentTime, arrivals, stop_id = MTAAPICall(route, stationCodes)

    context = {
        "route": route,
        "stopname": station,
        "stop_id": stop_id,
        "direction": directiondict[direction],
        "arrivals": [round(((x - currentTime)/60), 2) for x in arrivals],
        "currentTime": str(time.ctime(currentTime))
    }

    return render(request, "subwayFinder/arrival.html", context)


def api(request, route, stopcode):
    # Make API call to MTA, stopcode must be in list since it is a single value
    currentTime, arrivals, stop_id = MTAAPICall(route, [stopcode])
    APIreturn = {}
    if arrivals:  # If there are arrivals
        for i in range(len(arrivals)):
            APIreturn[i] = round(((arrivals[i]-currentTime)/60), 2)
    else:  # Return None if no trains coming
        APIreturn[0] = None
    return JsonResponse(APIreturn)  # Returns train number as key and arrival time in minutes as the value


def MTAAPICall(route, stopcodes):
    # Helper function to make request to MTA GFTS API
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id=1'.format(mta_api_key))
    feed.ParseFromString(response.content)
    currentTime = feed.header.timestamp  # Time of API call
    arrivals = []  # List of subway arrival times
    stationcode = 'N/A'  # If station code not found, return N/A

    for entity in feed.entity:  # For each trip in the response
      if entity.trip_update.trip.route_id == route:  # Matches the correct subway line
          for stop in (entity.trip_update.stop_time_update):  # Parse each stop for all active subways in the correct subway line
            for possibleStation in stopcodes:  # Parse each station code for the correct station (each station can have multiple station codes)
                if stop.stop_id == (possibleStation):  # Matches the direction and station
                    stationcode = stop.stop_id  # If station code is matched, assign the correct station code
                    arrivals.append(stop.arrival.time)  # Add arrival time of train to list
    return currentTime, arrivals, stationcode  # Return API call time, list of arriving times, and correct station code
