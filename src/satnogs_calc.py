from src import satnogs_api
from src import satnogs_selection
from src import tle
from src import flightPath
import skyfield  # TLE calculation
import ephem  # TLE calculation
from skyfield.api import EarthSatellite
from datetime import datetime



"""
 Satellite elements go rapidly out of date. You will want to pay attention to the “epoch”
 — the date on which an element set is most accurate — of every TLE element set you use. 
 Elements are only useful for a week or two on either side of the epoch date. 
 For later dates, you will want to download a fresh set of elements. 
 For earlier dates, you will want to pull an old TLE from the archives. 
"""


def getPasses(tleList: [tle.tle], latLong: (float, float), startDatetime: datetime, endDatetime: datetime) -> [flightPath]:
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
