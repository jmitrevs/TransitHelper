"""
test the interface to the bus tracker
"""

import unittest

from TransitHelper.BusTrackerInterface import *

import logging
#logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("testBustTrackerInterface")

class TestParsing(unittest.TestCase):

    def test_interfaceFuncs(self):
        """
        Just do basic calls to the interface functions to make sure no
        exceptions are thrown
        """
        getTime()
        getRoutes()
        getVehiclesVIDs("8130")
        getVehiclesRoutes("72")
        getDirections("72")
        getStops("72", "Westbound")
        getPatternsRoute("72")
        getPatternsPIDs("96")
        getPredictionsStops("943", "72")
        getPredictionsVIDs("8130")
