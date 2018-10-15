import csv
from math import radians, cos, sin, asin, sqrt, fabs

def haversin(theta):
    s = sin(theta / 2)
    return s * s

# get distance(in meter) between two geo points
def getDistance(lat0, lng0, lat1, lng1):
    lat0 = radians(lat0)
    lng0 = radians(lng0)
    lat1 = radians(lat1)
    lng1 = radians(lng1)

    dlat = fabs(lat0 - lat1)
    dlng = fabs(lng0 - lng1)
    h = haversin(dlat) + cos(lat0) * cos(lat1) * haversin(dlng)
    distance = 2 * 6371 * asin(sqrt(h)) * 1000

    return distance

x0 = 1
y0 = 1

def InCricle(x,y):
    return sqrt()

stations = csv.reader(open('dist_btwn_pts.csv','r'))
print(list(stations))