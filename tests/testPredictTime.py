"""
test the interface to the bus tracker
"""

import unittest

from TransitHelper.PredictTime import *

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
log = logging.getLogger(__name__)


class TestPrediction(unittest.TestCase):

    def test_predictions(self):
        """
        Check the prediction going from Harrison&Western to North&Sheffield
        via the Western and North Ave buses
        """
        # test Western Ave segment
        western = predictSegmentTime((8373, 17404, set()))
        log.info(f"Western segment: {western}")
        
        # test North Ave segment
        north = predictSegmentTime((894, 910, set()))
        log.info(f"North segment: {north}")

        
        # test combined
        combined = predictTripTime(((8373, 17404, set()), (894, 910, set())))
        log.info(f"Combined: {combined}")
        
