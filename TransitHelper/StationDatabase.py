"""
A database of which route statinos are on. Now estimate only some
"""

import TransitHelper.BusTrackerInterface as bi
import enum

class Categories(enum.IntEnum):
    """ The frequency categories for buses
    """
    INFREQUENT = 1
    MEDIUM = 2
    FREQUENT = 3
    RUSH = 4  # rush-hour (usually extra frequent)


def stopsSet(route, direction):
    """ return a set of the stop IDs for a route
    """
    stops = bi.getStops(route, direction)
    return set([int(stop["stpid"]) for stop in stops])


def stopsSetPair(route, direction):
    """ return a set of the stop IDs for a route
    """
    stops = bi.getStops(route, direction)
    return set([(int(stop["stpid"]), route) for stop in stops])


# don't include route number
RUSH = stopsSet("X49", "Northbound") | stopsSet("X49", "Southbound")
FREQUENT = stopsSet("49", "Northbound") | stopsSet("49", "Southbound")
MEDIUM = stopsSet("72", "Eastbound") | stopsSet("72", "Westbound")
INFREQUENT = stopsSet("73", "Eastbound") | stopsSet("73", "Westbound")

# include route number
RUSH_PAIR = stopsSetPair("X49", "Northbound") | stopsSetPair("X49", "Southbound")
FREQUENT_PAIR = stopsSetPair("49", "Northbound") | stopsSetPair("49", "Southbound")
MEDIUM_PAIR = stopsSetPair("72", "Eastbound") | stopsSetPair("72", "Westbound")
INFREQUENT_PAIR = stopsSetPair("73", "Eastbound") | stopsSetPair("73", "Westbound")
