#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The interface to the bus tracker information
"""

import requests
from TransitHelper.Tokens import BUS_TOKEN

ADDRESS = "http://www.ctabustracker.com/bustime/api/v2/"

PARAMS = {"key": BUS_TOKEN, "format": "json"}

def _makeRequest(command, extraParams={}):
    r = requests.get(ADDRESS + command, params={**PARAMS, **extraParams})
    r.raise_for_status()
    response = r.json()["bustime-response"]
    if "error" in response:
        raise RuntimeError(response["error"])
    return response

def getTime():
    """ 
    Get the time as reported by the tracker, format "YYYYMMDD HH:MM:SS"
    """
    return _makeRequest("gettime")["tm"]

def getRoutes():
    """ Get a list of routes
    """
    return _makeRequest("getroutes")["routes"]

def getVehiclesVIDs(vids):
    """ 
    Get a list of vihicles (with long/lat, timestamp, route)
    with the given VIDs (comma-separated text)
    """
    return _makeRequest("getvehicles", {"vid": vids, "tmres": "s"})["vehicle"]

def getVehiclesRoutes(routes):
    """ 
    Get a list of vihicles (with long/lat, timestamp, route)
    on the given routes (comma-separated text)
    """
    return _makeRequest("getvehicles", {"rt": routes, "tmres": "s"})["vehicle"]

def getDirections(route):
    """ Get the directions for a route
    """
    return _makeRequest("getdirections", {"rt": route})["directions"]

def getStops(route, direction):
    """ Get the stops (with long/lat) for a given route and direction
    """
    return _makeRequest("getstops", {"rt": route, "dir": direction})["stops"]

def getPatternsRoute(route):
    """ Get the patterns for a given route
    """
    return _makeRequest("getpatterns", {"rt": route})["ptr"]

def getPatternsPIDs(pid):
    """ Get the patterns for given PIDs (comma-separated list)
    """
    return _makeRequest("getpatterns", {"pid": pid})["ptr"]

def getPredictionsStops(stop, routes=None):
    """ 
    Get the predictions for given stops (comma-separated list), 
    optionally restricting it to given routes (comma-seperated list)
    """
    pars = {"stpid": stop, "tmres": "s"}
    if routes:
        pars["rt"] = routes
    return _makeRequest("getpredictions", pars)["prd"]

def getPredictionsVIDs(vid):
    """ 
    Get the predictions for given vehicle IDs (comma-separated list)
    """
    pars = {"vid": vid, "tmres": "s"}
    return _makeRequest("getpredictions", pars)["prd"]
