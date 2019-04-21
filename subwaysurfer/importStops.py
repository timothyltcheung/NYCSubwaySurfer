import csv
from subwayFinder.models import StationStop

CSV_path = r'.\stop.csv'

with open(CSV_path) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row[0]) == 3:    #Eliminates redundancies of N and S
            stop = StationStop(stopcode = row[0], stopname = row[2])
            stop.save()

exit()
