import time
import numpy
from skyfield.timelib import Time
from skyfield.toposlib import wgs84
from src import flightPath, satnogs_api, satnogs_selection
from skyfield.api import EarthSatellite, load
from datetime import datetime


class flightPath(object):
    def __init__(self):
        self.name: str = ""
        self.tle1: str = ""
        self.tle2: str = ""
        self.satellite: EarthSatellite = None
        self.duration: float = 0
        self.freq: float = 0
        self.animationSpeed: float = 0
        self.path: list = []
        self.interval: list = []
        self.elevation: list = []
        self.beginTime: float = 0
        self.radioPass: list = []

    def __init__(self, tle0: str, tle1: str, tle2: str, duration: float, freq: float):
        """

        :param tle0: satellite name
        :param tle1: tle response line1
        :param tle2: tle response line2
        :param duration: duration of flight path in sec
        :param freq: update freq per minute
        """

        self.name: str = tle0
        self.tle1: str = tle1
        self.tle2: str = tle2
        self.satellite: EarthSatellite = None
        self.duration: float = float(duration)
        self.freq: float = float(freq)
        self.animationSpeed: float = freq * 60.0 * 1000

        self.path: list = []
        self.interval: list = []
        self.elevation: list = []
        self.beginTime: float = 0
        self.radioPass: list = []

        self.findLatLongPath()

    def findLatLongPath(self) -> ([], [], ()):
        """

        :return:
        """
        self.satellite = EarthSatellite(self.tle1, self.tle2, self.name, load.timescale())
        ts = load.timescale()
        t = ts.now()
        self.beginTime = t
        start = t.utc.second
        end = start + self.duration
        self.interval = ts.utc(t.utc.year, t.utc.month, t.utc.day, t.utc.hour, t.utc.minute,
                               numpy.arange(start, end, self.freq * 60))
        location = self.satellite.at(self.interval)
        LatLong = wgs84.subpoint(location)

        self.path = (LatLong.latitude.degrees, LatLong.longitude.degrees, LatLong.elevation.au)


    def findHorizonTime(self, rx: wgs84.latlon = wgs84.latlon(33.643831, -117.841132, elevation_m=17)) -> list:
        now = self.beginTime
        ts = load.timescale()
        start = now
        t = now.utc
        end = ts.utc(t.year, t.month, t.day, t.hour, t.minute, t.second + self.duration)
        condition = {"bare": 0, "marginal": 25.0, "good": 50.0, "excellent": 75.0}
        degree = condition["bare"]  # peak is at 90
        t, events = self.satellite.find_events(rx, start, end, altitude_degrees=degree)

        # for ti, event in zip(t, events):
        #     name = (f'rise above {degree}°', 'culminate', f'set below {degree}°')[event]
        #     print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

        intervals = []
        for i in range(0, len(events), 3):
            try:
                t[i + 2]
            except IndexError:
                break
            else:
                datetime_rise = Time.utc_datetime(t[i])
                datetime_peak = Time.utc_datetime(t[i + 1])
                datetime_set = Time.utc_datetime(t[i + 2])
                t0 = ts.utc(datetime_rise.year, datetime_rise.month, datetime_rise.day, datetime_rise.hour,
                            datetime_rise.minute, datetime_rise.second)

                diff = numpy.float64((datetime_set - datetime_rise).total_seconds())
                t0_sec = t0.utc.second
                t1_sec = t0_sec + diff
                intervals.append(
                    (ts.utc(t0.utc.year, t0.utc.month, t0.utc.day, t0.utc.hour, t0.utc.minute,
                            numpy.arange(t0_sec, t1_sec, 1)),
                     datetime_peak))

        # print("found: ", len(interval))
        # print("finding horizon for duration of 3 days took: ", time.perf_counter() - fuctimer)
        return sorted(intervals, key=lambda x: -len(x[0]))


    def findHorizonPath(self, intervals: list):
        for t in intervals:
            location = self.satellite.at(t[0])
            LatLong = wgs84.subpoint(location)
            self.radioPass.append((LatLong.latitude.degrees, LatLong.longitude.degrees, LatLong.elevation.au))
