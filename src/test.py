from matplotlib import pyplot

from src import satnogs_api, satnogs_selection, satnogs_calc, location_input
from skyfield.api import EarthSatellite, load
import requests
import pytz
import numpy



def testLocation() -> None:
    """

    :return:
    """

    url = location_input.getURL()
    print(url)
    response = requests.get(url).json()
    print("UCI:", response["resourceSets"][0]["resources"][0]["point"]["coordinates"])


def testGetTLE() -> [str, str]:
    """

    :return:
    """

    allSatellite = satnogs_api.getSatellites()
    filteredSatellite = satnogs_selection.satelliteFilter(allSatellite)
    sortedSatellite = satnogs_selection.sortMostRecent(filteredSatellite)
    TLEs = satnogs_selection.tleFilter(sortedSatellite)
    line1 = ""
    line2 = ""
    for l in TLEs:
        if "amicalsat" == str(l["tle0"]).lower():
            line0 = l["tle0"]
            line1 = l["tle1"]
            line2 = l["tle2"]

    ts = load.timescale()
    t = ts.now()
    print("Satellite: ", l["tle0"])
    print("Curr Time:", t.utc_strftime())

    return [line0, line1, line2]


def testGeneratePath(lines: [str, str, str]):
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    xyz = []
    x = []
    y = []
    z = []
    start = 0
    end = 120

    for minute in range(start, end):
        t = ts.utc(2021, 5, 22, 10, minute, 0)  # how can I specify time in a better way than doing this???
        # need to build some kind of time array
        geocentric = satellite.at(t)
        xyz.append(geocentric.position.km)
        x.append(geocentric.position.km[0])
        y.append(geocentric.position.km[1])
        z.append(geocentric.position.km[2])

    print("flightPath start time: ", ts.utc(2021, 5, 22, 10, start, 0).utc_strftime())
    print("flightPath end time: ", ts.utc(2021, 5, 22, 10, end - 1, 0).utc_strftime())

    print(x)
    print(y)
    print(z)

    for l in xyz:
        print(l)

    pyplot.plot(x, y)
    pyplot.show()


def testTimeZoneConversion():
    """

    :return:
    """
    pacificTimeZone = pytz.timezone("US/Pacific")
    centralTimeZone = pytz.timezone("US/Central")
    ts = load.timescale()
    t = ts.now()
    dt = t.utc_datetime()
    cst = t.astimezone(centralTimeZone)
    pst = t.astimezone(pacificTimeZone)
    print("Curr Time in UTC: ", dt)
    print("Curr Time in CST: ", cst)
    print("Curr Time in PST: ", pst)


def testPlot():
    ts = load.timescale()
    ts.utc(range(1900, 1950))  # Fifty years 1900–1949
    ts.utc(1980, range(1, 25))  # 24 months of 1980 and 1981
    ts.utc(2005, 5, [1, 11, 21])  # 1st, 11th, and 21st of May

    # Negative values work too!  Here are the
    # ten seconds crossing the 1974 leap second.
    ts.utc(1975, 1, 1, 0, 0, range(-5, 5))

    t = ts.utc(2020, 6, 16, 7, range(4))
    for s in t.utc_strftime('%Y-%m-%d %H:%M'):
        print(s)

    planets = load('de421.bsp')
    earth = planets['earth']

    t = ts.utc(2014, 1, 1)
    pos = earth.at(t).position.au
    print(pos)

    days = [1, 2, 3, 4]
    t = ts.utc(2014, 1, days)
    pos = earth.at(t).position.au
    print(pos)

    x, y, z = pos  # four values each
    pyplot.plot(x, y)  # example matplotlib call
    pyplot.show()



"""
driver
"""

response = testGetTLE()  # loading from API every time is slow, should load from a file instead
testGeneratePath(response)

# testPlot()

# testTimeZoneConversion()
