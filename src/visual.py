from matplotlib import pyplot
from src import satnogs_calc


def updatePath(lat: [], long: [], start: (float, float)):
    fig, ax = pyplot.subplots(figsize=(20, 10))
    ax.plot(long, lat, 'black')
    ax.annotate("▀█▀", start, color='red')
    ax.set(xlabel='longitude', ylabel='latitude')
    ax.grid()


def updateOrbit(x: [], y: [], z: [], h: []):
    pyplot.figure(2)
    pyplot.axes(projection='3d', xlabel='x (km)', ylabel='y (km)', zlabel='z (km)')
    pyplot.plot(x, y, z, 'red')
    pyplot.title("Geocentric Flight Path")

    pyplot.figure(3)
    pyplot.axes(xlabel='time (sec)', ylabel='altitude (km)')
    pyplot.plot(h, 'blue')
    pyplot.title("Flight Altitude")
    pyplot.grid()


duration = 4 * 3600
resolution = 4.0

tle = satnogs_calc.loadTLE()
response = satnogs_calc.getTLELineResponse(tle, "amicalsat")
lat, long, start = satnogs_calc.getLatLongPath(response, duration, resolution)
x, y, z, h = satnogs_calc.getOrbitPath(response, duration, resolution)
updatePath(lat, long, start)
updateOrbit(x, y, z, h)
pyplot.show()
