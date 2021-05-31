import time
from matplotlib import pyplot
from src import satnogs_api, satnogs_selection, satnogs_calc, location_input, satnogs_export
from skyfield.api import EarthSatellite, load, wgs84, Time
import requests
import pytz
import numpy
import matplotlib.pyplot as plt
from src import flightPath

import numpy as np
from matplotlib.animation import FuncAnimation


def testAnimation():
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                        init_func=init, blit=True)
    plt.show()


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
            print("Satellite: ", l["tle0"])
            break

    ts = load.timescale()
    t = ts.now()
    print("Curr Time:", t.utc_strftime())

    return [line0, line1, line2]


def testCurrLocation(lines: [str, str, str]):
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    currLoc = satellite.at(ts.now())
    latlong = wgs84.subpoint(currLoc)
    print("curr XYZ: ", currLoc.position.km[0], currLoc.position.km[1], currLoc.position.km[2])
    print("curr LatLong: ", latlong.latitude, latlong.longitude)


def testLatLongPath(lines: [str, str, str]) -> ([], []):
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    t = ts.now()
    start = t.utc.second
    end = start + 3600
    lat = []
    long = []

    for sec in numpy.arange(start, end, 0.25):
        currTime = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.minute, sec)
        currLoc = satellite.at(currTime)
        currLatLong = wgs84.subpoint(currLoc)
        lat.append(currLatLong.latitude.degrees)
        long.append(currLatLong.longitude.degrees)

    # print(lat, long)

    fig, ax = pyplot.subplots(figsize=(20, 10))
    ax.plot(long, lat)
    ax.set(xlabel='longitude', ylabel='latitude')
    ax.grid()
    pyplot.show()

    return lat, long


def testGeneratePath(lines: [str, str, str]):
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    xyz = []
    x = []
    y = []
    z = []
    h = []
    start = 0
    end = int(1 / 4 * 1440)  # 6 hr
    # end = 30 * 1440  # a month

    for minute in range(start, end):
        # how can I specify time in a better way than doing this???
        t = ts.utc(2021, 5, 22, 0, minute, 0)
        # need to build some kind of time array
        geocentric = satellite.at(t)
        # xyz.append(geocentric.position.km)
        x.append(geocentric.position.km[0])
        y.append(geocentric.position.km[1])
        z.append(geocentric.position.km[2])
        p = numpy.array((geocentric.position.km[0], geocentric.position.km[1], geocentric.position.km[2]))
        o = numpy.array((0, 0, 0))
        h.append(numpy.linalg.norm(p - o))

    print("flightPath start time: ", ts.utc(2021, 5, 22, 10, start, 0).utc_strftime())
    print("flightPath end time: ", ts.utc(2021, 5, 22, 10, end - 1, 0).utc_strftime())

    pyplot.figure(1)
    pyplot.axes(projection='3d', xlabel='x (km)', ylabel='y (km)', zlabel='z (km)')
    pyplot.plot(x, y, z, 'red')
    pyplot.title("Geocentric Flight Path")

    pyplot.figure(2)
    pyplot.axes(xlabel='time (min)', ylabel='altitude (km)')
    pyplot.plot(h, 'blue')
    pyplot.title("Flight Altitude")
    pyplot.grid()
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


def testFlightPath():
    f = satnogs_calc.loadTLE()
    sats = []
    totalT = 0
    count = 0
    for r in f:
        s = flightPath.flightPath(r['tle0'], r['tle1'], r['tle2'], 5.0 * 3600, 1 / 2)
        totalT += s.calcTimer
        print(count, "/", len(f))
        count += 1
        sats.append(s)

    for r in sats:
        print(r.name, len(r.path[0]))

    print(totalT)


def testAmical():
    tle0 = "AMICALSAT"
    tle1 = "1 46287U 20061R   21146.44766273  .00000677  00000-0  44968-4 0  9994"
    tle2 = "2 46287  97.4881 220.1957 0003468 144.5473 215.5988 15.10442191 40023"
    return EarthSatellite(tle1, tle2, tle0, load.timescale())


def testHorizon(r):
    # TODO visit https://www.n2yo.com/passes/?s=46287&a=1 and compare result
    fuctimer = time.perf_counter()
    irvine = wgs84.latlon(33.643831, -117.841132, elevation_m=17)  # receiver location object
    now = load.timescale().now().utc
    ts = load.timescale()
    start = ts.now()
    end = ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second + 3 * 24 * 3600)

    # satellite = testAmical()  # satellite object
    # print(satellite)

    satellite = EarthSatellite(r['tle0'], r['tle1'], r['tle2'], ts)
    print(satellite)

    condition = {"bare": 0, "marginal": 25.0, "good": 50.0, "excellent": 75.0}
    degree = condition["marginal"]  # peak is at 90
    t, events = satellite.find_events(irvine, start, end, altitude_degrees=degree)

    zero_degree = 0
    t_wide,  events_wide = satellite.find_events(irvine, start, end, altitude_degrees=zero_degree)

    for ti, event in zip(t, events):
        name = (f'rise above {degree}°', 'culminate', f'set below {degree}°')[event]
        print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

    """
    [y0 = 20, y1 = 31]
    2021 Jun 01 18:20:05 rise above 0°
    2021 Jun 01 18:26:03 culminate
    2021 Jun 01 18:31:58 set below 0°

    2021 Jun 01 19:55:54 rise above 0°
    2021 Jun 01 19:59:52 culminate
    2021 Jun 01 20:03:49 set below 0°
    
    [x0 = 23, x1 = 28]
    2021 Jun 01 18:23:56 rise above 25.0°
    2021 Jun 01 18:26:03 culminate
    2021 Jun 01 18:28:10 set below 25.0°
    
    for event in bare:
        y0, y1 = event[i], event[i + 2]
        for e in marginal:
            x0, x1 = e[i], e[i + 2]
            if x0 > y0 and x1 < y1:
                intervals.append([y0 = 20, y1 = 31])
    """

    wide_intervals = []
    for i in range(0, len(events_wide), 3):
        datetime_rise = Time.utc_datetime(t_wide[i])
        datetime_peak = Time.utc_datetime(t_wide[i + 1])
        datetime_set = Time.utc_datetime(t_wide[i + 2])
        rise = ts.utc(datetime_rise.year, datetime_rise.month, datetime_rise.day, datetime_rise.hour,datetime_rise.minute, datetime_rise.second)
        diff = numpy.float64((datetime_set - datetime_rise).total_seconds())
        rise_sec = rise.utc.second
        set_sec = rise_sec + diff
        wide_intervals.append((ts.utc(rise.utc.year, rise.utc.month, rise.utc.day, rise.utc.hour, rise.utc.minute, numpy.arange(rise_sec, set_sec, 60)),datetime_peak))

    intervals = []
    match_intervals = []
    for i in range(0, len(events), 3):
        datetime_rise = Time.utc_datetime(t[i])
        datetime_peak = Time.utc_datetime(t[i + 1])
        datetime_set = Time.utc_datetime(t[i + 2])

        rise = ts.utc(datetime_rise.year, datetime_rise.month,datetime_rise.day, datetime_rise.hour,datetime_rise.minute, datetime_rise.second)
        diff = numpy.float64((datetime_set - datetime_rise).total_seconds())
        rise_sec = rise.utc.second
        set_sec = rise_sec + diff
        interval = (ts.utc(rise.utc.year, rise.utc.month, rise.utc.day,rise.utc.hour, rise.utc.minute,numpy.arange(rise_sec, set_sec, 60)),datetime_peak)
        intervals.append(interval)

        for wi in wide_intervals:
            if wi[1] == interval[1]:
                match_intervals.append(wi)

    assert len(intervals) == len(match_intervals)

    print("found: ", len(match_intervals))
    print("finding horizon for duration of 3 days took: ", time.perf_counter() - fuctimer)
    return sorted(intervals, key=lambda x: -len(x[0]))


def testTimeArray():
    # TODO replace all separate time object to time array
    now = load.timescale().now().utc
    ts = load.timescale()
    pacificTimeZone = pytz.timezone("US/Pacific")

    i, j, r = 0, 59, 1 / 4.0
    for sec in numpy.arange(i, j, r):  # this creates (j-i)/60 number of load.timescale() object!!!
        curr = ts.utc(now.year, now.month, now.day, now.hour, now.minute, sec)
        # print(curr.astimezone(pacificTimeZone))
        print(float(sec))

    #  was interval = yr=2021, month=5, day=29, hour=13, min=37, sec=00
    #  now interval = yr=2021, month=5, day=29, hour=13, min=37, sec=range(0,3600)
    interval = ts.utc(now.year, now.month, now.day, now.hour, now.minute, numpy.arange(i, j, r))
    # for t in interval.astimezone(pacificTimeZone):
    #     print(t)

    # print(interval.utc.second)
    # for i in range(len(interval.utc.second)):
    #     print(float(interval.utc.second[i]))


"""
driver
"""


# testTimeArray()

file = satnogs_export.loadTLE(satnogs_export.TLE_DIR)
path = []
count = 1

for r in file:
    # print(r['tle0'], r['tle1'], r['tle2'], "\n\n")
    testHorizon(r)


# testFlightPath()
# response = testGetTLE()  # loading from API every time is slow, should load from a file instead
# # testCurrLocation(response)
# # testGeneratePath(response)
# testLatLongPath(response)
# testAnimation()
