import time
import numpy
from skyfield.toposlib import wgs84
from src import flightPath, satnogs_api, satnogs_selection, satnogs_export
from skyfield.api import EarthSatellite, load
from datetime import datetime


"""
 Satellite elements go rapidly out of date. You will want to pay attention to the “epoch”
 — the date on which an element set is most accurate — of every TLE element set you use. 
 Elements are only useful for a week or two on either side of the epoch date. 
 For later dates, you will want to download a fresh set of elements. 
 For earlier dates, you will want to pull an old TLE from the archives. 
"""


def loadTLE() -> [dict]:
    # TODO: instead of loading from API, load from file
    """
    :return: list of dict containing TLEs
    """
    timer = time.perf_counter()
    allSatellite = satnogs_api.getSatellites()
    filteredSatellite = satnogs_selection.satelliteFilter(allSatellite)
    sortedSatellite = satnogs_selection.sortMostRecent(filteredSatellite)
    print(f'loadTLE took {time.perf_counter() - timer:.3f} second to process')
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
    :return: list of LatLongs, starting location, current time, satellite name

    """
    timer = time.perf_counter()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second
    end = start + duration

    y = wgs84.subpoint(satellite.at(t)).latitude.degrees
    x = wgs84.subpoint(satellite.at(t)).longitude.degrees

    interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute, numpy.arange(start, end, resolution*60))
    location = satellite.at(interval)
    LatLong = wgs84.subpoint(location)


    print(f'getLatLongPath {time.perf_counter() - timer:.3f} second to process')
    return LatLong.latitude.degrees, LatLong.longitude.degrees, (x, y), t, lines[0]


def getOrbitPath(lines: [], duration: float = 4.0 * 3600, resolution: float = 4.0) -> ([], [], [], []):
    """

    :param lines:
    :param duration:
    :param resolution:
    :return:
    """

    timer = time.perf_counter()
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second
    end = start + duration
    h = []

    interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute, numpy.arange(start, end, resolution * 60))
    location = satellite.at(interval)
    x = location.position.km[0]
    y = location.position.km[1]
    z = location.position.km[2]

    for i in range(len(x)):
        h.append(numpy.linalg.norm(numpy.array([x[i], y[i], z[i]]) - numpy.array([0, 0, 0])))

    print(f'getOrbitPath {time.perf_counter() - timer:.3f} second to process')
    return x, y, z, h


def overlap(path: flightPath.flightPath, observer: wgs84.latlon = wgs84.latlon(33.643831, -117.841132)):
    d = satnogs_export.loadTLE('D:\\tle.save')
    sats = dict()
    for r in d:
        sats[r['tle0']] = flightPath.flightPath(r['tle0'], r['tle1'], r['tle2'], 3.0 * 3600, 3)

    pass




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


lines = ["AMICALSAT", "1 46287U 20061R   21146.44766273  .00000677  00000-0  44968-4 0  9994", "2 46287  97.4881 "
                                                                                               "220.1957 0003468 "
                                                                                               "144.5473 215.5988 "
                                                                                               "15.10442191 40023"]
getOrbitPath(lines)

