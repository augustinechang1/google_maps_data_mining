
from geographiclib.constants import Constants
from geographiclib.geodesic import Geodesic

address = ""
keyword = ""

lat1 = 40.747683
lon1 = -73.954419

d = 10/12*1609.34
b = 180


def getEndpoint(lat1, lon1, bearing, d):
    geod = Geodesic(Constants.WGS84_a, Constants.WGS84_f)
    d = geod.Direct(lat1, lon1, bearing, d)
    return d['lat2'], d['lon2']

print(getEndpoint(lat1, lon1, b, d))