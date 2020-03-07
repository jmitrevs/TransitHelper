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
    return r.json()["bustime-response"]

def getTime():
    """ 
    Get the time as reported by the tracker, format "YYYYMMDD HH:MM:SS"
    """
    return _makeRequest("gettime")["tm"]

def getRoutes():
    """ Get a list of routes
    """
    return _makeRequest("getroutes")["routes"]

