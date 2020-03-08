"""
Varlius helpers
"""
import math
from datetime import datetime, timedelta


def distance(lat1, lon1, lat2, lon2):
    """
    The haversine formula for distances
    (from Stack Overflow, translated to python)
    """
    EARTH_RADIUS = 6371  # km

    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = (math.sin(dLat/2)**2 +
         math.sin(dLon/2)**2 * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS * c


def toDatetime(timestring):
    """ return the python datatime given a timestring
    """
    return datetime.strptime(timestring, "%Y%m%d %H:%M:%S")


def uncertaintyEst(currTime, estArrivalTime):
    """
    This estimates the uncertainty in estimating the arrival time
    given the remaining time till the arrival.

    Input:
      currTime:datetime - the current time
      estArrivalTime:datetime - the estimated arrival time

    Output:
      pair (earlyTime:datetime, lateTime:datetime),
         the range of times the bus should arrive

    Put initial prediction; to tune/train with data
    """

    diff = estArrivalTime - currTime
    secEstimate = 120 + diff.total_seconds()/300
    estimate = timedelta(seconds=secEstimate)
    return (estArrivalTime - estimate, estArrivalTime + estimate)
