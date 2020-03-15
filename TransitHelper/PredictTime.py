#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple routine to predict the transit time
"""

from datetime import datetime, timedelta
from dataclasses import dataclass
import typing

import TransitHelper.BusTrackerInterface as bi
import TransitHelper.Utilities as utils


@dataclass
class Trip:
    """ information about a given trip
    """
    startStop: str
    endStop: str
    startTime: datetime
    endTimeMin: datetime
    endTimeMax: datetime
    vidsMin: typing.List   # The VIDs for the fastest trip
    vidsMax: typing.List   # The VIDs for the slowest trip


def predictTripTime(listOfSegments, startTime=None):
    """
    Input: An iterable of tuples, (start station, end station, {routes} ) for the route
       If routes is empty, then any rout is fine
    Output: a Trip
    """

    now = utils.toDatetime(bi.getTime())

    if startTime is None:
        startTime = now

    totalPred = None

    # for segment time predictions, always use predictions from now.
    # CTA only provides predictions in a limited time in the future, so this
    # extends the range that the predictions can be used. Further out
    # one should switch to using the bus schedule (currently not implmented)

    for segment in listOfSegments:
        if not totalPred:
            # first segment
            segTrip = predictSegmentTime(segment, startTime)
            print(segTrip)
            if segTrip is None:
                # There are no possibilites or predictions
                return None
            totalPred = segTrip
        else:
            # already have a segment
            walkTime = predictWalk(totalPred.endStop, segment[0])
            segTrip = predictSegmentTime(segment, now, useBusStartTime=True)  # using current time

            # calculating earliest time
            bestVidMin = predictBusVID(segment, totalPred.endTimeMin + walkTime[0])
            if bestVidMin is None:
                # no trip or prediction available (can improve in the future)
                return None
            totalPred.endTimeMin += walkTime[0] + (segTrip.endTimeMin - segTrip.startTime)
            totalPred.vidsMin.append(vestVidMin)

            # calculatign the latest time
            bestVidMax = predictBusVID(segment, totalPred.endTimeMax + walkTime[1])
            if bestVidMax is None:
                # No prediction available if connection is missed (in future version, revert to schedule)
                totalPred.endTimeMax = datetime.max
            else:
                totalPred.endTimeMax += walkTime[1] + (segTrip.endTimeMax - segTrip.startTime)
                totalPred.vidsMax.append(vestVidMax)

    return totalPred


def predictSegmentTime(segment, startTime=None, useBusStartTime=False):
    """
    Input: A (start station, end station, {buses}) tuple on a single route
    (Use any bus if buses is an empty set, or any empyt iterable), and the start time (None=now)
    if useBusStartTime is True, time uncertainty is assuming start time is exactly known
    Output: a Trip
    """

    if startTime is None:
        startTime = utils.toDatetime(bi.getTime())

    startPreds = bi.getPredictionsStops(segment[0])
    endPreds = bi.getPredictionsStops(segment[1])

    bestVid = None
    bestEnd = datetime.max
    bestStart = None

    for startPred in startPreds:
        if segment[2] and startPred["rt"] not in segment[2]:
            # if want to take only certain routes
            continue
        startPredTime = utils.toDatetime(startPred["prdtm"])
        if startPredTime > startTime:
            vid = startPred["vid"]
            bestStart = startPredTime
            for endPred in endPreds:
                if vid == endPred["vid"]:
                    predTime = utils.toDatetime(endPred["prdtm"])
                    if predTime < bestEnd:
                        bestVid = vid
                        bestEnd = predTime

    if bestVid:
        uncStartTime = bestStart if useBusStartTime else startTime
        earliest, latest = utils.uncertaintyEst(uncStartTime, bestEnd)
        return Trip(segment[0], segment[1], bestStart, earliest, latest, [bestVid], [bestVid])
    else:
        # no trip available or no prediction available (can add checking schedule in the future)
        return None


def predictWalk(stopBegin, stopEnd):
    """
    predict how long the walk is
    return (min, max) time
    """
    if stopBegin == stopEnd:
        return (timedelta(seconds=10), timedelta(seconds=30))
    else:
        # for now just estimate the same
        return (timedelta(seconds=10), timedelta(seconds=300))


def predictBusVID(segment, startTime=None):
    """
    Input: A (start station, end station, {buses}) tuple on a single route
    (Use any bus if buses is an empty set, or any empyt iterable), and the start time (None=now)
    Returns the next VID for this trip
    """
    if startTime is None:
        startTime = utils.toDatetime(bi.getTime())

    startPreds = bi.getPredictionsStops(segment[0])

    bestVid = None
    bestStart = datetime.max

    for startPred in startPreds:
        if segment[2] and startPred["rt"] not in segment[2]:
            # if want to take only certain routes
            continue
        startPredTime = utils.toDatetime(startPred["prdtm"])
        if startPredTime > startTime and startPredTime < bestStart:
            bestVid = startPred["vid"]
            bestStart = startPredTime

    return bestVid
