from src import satnogs_api
from src import satnogs_selection
from src import tle
from src import flightPath
import skyfield  # TLE calculation
import ephem  # TLE calculation
from datetime import datetime


def getPasses(tleList: [tle.tle], latLong: (float, float), startDatetime: datetime, endDatetime: datetime) -> [flightPath]:
    """

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
