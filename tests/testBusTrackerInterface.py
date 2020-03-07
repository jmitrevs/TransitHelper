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
        log.debug(getTime())
        log.debug(getRoutes())
        

