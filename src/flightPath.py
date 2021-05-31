import time
import numpy
from skyfield.toposlib import wgs84
from src import flightPath, satnogs_api, satnogs_selection
from skyfield.api import EarthSatellite, load
from datetime import datetime


class flightPath(object):
    def __init__(self):
        self.name = ""
        self.tle1 = ""
        self.tle2 = ""
        self.duration = 0
        self.freq = 0
        self.animationSpeed = 0
        self.path = None
        self.beginTime = 0
        self.calcTimer = 0

    def __init__(self, tle0: str, tle1: str, tle2: str, duration: float, freq: float):
        """

        :param tle0: satellite name
        :param tle1: tle response line1
        :param tle2: tle response line2
        :param duration: duration of flight path in sec
        :param freq: update freq per minute
        """

        self.name = tle0
        self.tle1 = tle1
        self.tle2 = tle2
        self.duration = float(duration)
        self.freq = float(freq)
        self.animationSpeed = freq * 60.0 * 1000

        self.calcTimer = time.perf_counter()
        self._calcLatLongPath()
        self.calcTimer = time.perf_counter() - self.calcTimer


    def _calcLatLongPath(self) -> ([], [], ()):
        """

        :return:
        """
        satellite = EarthSatellite(self.tle1, self.tle2, self.name, load.timescale())
        ts = load.timescale()
        t = ts.now()
        start = t.utc.second
        end = start + self.duration
        interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute,
                          numpy.arange(start, end, self.freq * 60))
        location = satellite.at(interval)
        LatLong = wgs84.subpoint(location)

        self.path = (LatLong.latitude.degrees, LatLong.longitude.degrees)
        self.elevation = LatLong.elevation.au
        self.beginTime = t

    def _calcXYZPath(self) -> ([], [], ()):
        """

        :return:
        """
        satellite = EarthSatellite(self.tle1, self.tle2, self.name, load.timescale())
        ts = load.timescale()
        t = ts.now()
        start = t.utc.second
        end = start + self.duration
        interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute,
                          numpy.arange(start, end, self.freq * 60))
        location = satellite.at(interval)
        x = location.position.km[0]
        y = location.position.km[1]
        z = location.position.km[2]
        h = []

        for i in range(len(x)):
            h.append(numpy.linalg.norm(numpy.array([x[i], y[i], z[i]]) - numpy.array([0, 0, 0])))

        self.path = (x, y, z, h)
        self.beginTime = t
