import numpy
from skyfield.toposlib import wgs84
from src import flightPath, satnogs_api, satnogs_selection
from skyfield.api import EarthSatellite, load
from datetime import datetime


"""
 Satellite elements go rapidly out of date. You will want to pay attention to the “epoch”
 — the date on which an element set is most accurate — of every TLE element set you use. 
 Elements are only useful for a week or two on either side of the epoch date. 
 For later dates, you will want to download a fresh set of elements. 
 For earlier dates, you will want to pull an old TLE from the archives. 
"""


def loadTLE() -> dict:
    """

    :return:
    """
    allSatellite = satnogs_api.getSatellites()
    filteredSatellite = satnogs_selection.satelliteFilter(allSatellite)
    sortedSatellite = satnogs_selection.sortMostRecent(filteredSatellite)
    return satnogs_selection.tleFilter(sortedSatellite)


def getTLELineResponse(tleSet: [], target: str) -> []:
    """

    :param tleSet: set of TLEs from api
    :param target: name of desired Satellite
    :return: Two-line Element response
    """

    TLEs = tleSet
    name = ""
    line1 = ""
    line2 = ""
    for r in TLEs:
        if target.lower() == str(r["tle0"]).lower():
            name = r["tle0"]
            line1 = r["tle1"]
            line2 = r["tle2"]
            break

    return [name, line1, line2]


def getLatLongPath(lines: [], duration: float = 4.0 * 3600, resolution: float = 4.0) -> ([], [], ()):
    """

    :param lines: TLE response
    :param duration: flight duration
    :param resolution: number of calculation per second
    :return: list of LatLongs and starting location

    """
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second
    end = start + duration
    lat = []
    long = []
    y = wgs84.subpoint(satellite.at(t)).latitude.degrees
    x = wgs84.subpoint(satellite.at(t)).longitude.degrees

    for sec in numpy.arange(start - 600, end, resolution * 60.0):
        currTime = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute, sec)
        currLoc = satellite.at(currTime)
        currLatLong = wgs84.subpoint(currLoc)
        lat.append(currLatLong.latitude.degrees)
        long.append(currLatLong.longitude.degrees)

    return lat, long, (x, y), t


def getOrbitPath(lines: [], duration: float = 4.0 * 3600, resolution: float = 4.0) -> ([], [], [], []):
    """

    :param lines:
    :param duration:
    :param resolution:
    :return:
    """

    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second
    end = start + duration
    x = []
    y = []
    z = []
    h = []

    for sec in numpy.arange(start, end, resolution * 60.0):
        currTime = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute, sec)
        currLoc = satellite.at(currTime)
        x.append(currLoc.position.km[0])
        y.append(currLoc.position.km[1])
        z.append(currLoc.position.km[2])
        point = numpy.array((currLoc.position.km[0], currLoc.position.km[1], currLoc.position.km[2]))
        center = numpy.array((0, 0, 0))
        h.append(numpy.linalg.norm(point - center))

    return x, y, z, h


def getPasses(tleList: [], latLong: (float, float), startDatetime: datetime, endDatetime: datetime) -> [flightPath]:
    """
    get a list flightPath object of all passes over certain LatLong
    example: getPasses(tleList, "Irvine", ...) -> [ISS, AMICALSAT, BOBCATSAT, ....]

    :param tleList: A list of tle object
    :param latLong: latitude, longitude pair of ground station in degrees
    :param startDatetime: The start datetime wanted
    :param endDatetime: The end datetime wanted
    :return: A list of flightPath object

    """

    pass


def filterPasses(passList: [], elevation: float, horizonDegree: float, minDuration: int) -> [flightPath]:
    """

    :param passList: A list of tle object
    :param elevation: elevation of ground station in meters
    :param horizonDegree:
    :param minDuration: minDuration of pass in seconds
    :return: A list of flightPath object

    """
    pass
