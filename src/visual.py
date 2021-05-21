from matplotlib import pyplot
from src import satnogs_calc


def updatePath(lat: [float], long: [float], start: (float, float), timestamp) -> None:
    fig, ax = pyplot.subplots(figsize=(20, 10))
    ax.plot(long, lat, 'black')
    ax.annotate(f'▀█▀ {start[0]:.4f}, {start[1]:.4f} @ {timestamp.utc_strftime()}', start, color='red')
    ax.annotate(f'△ {"UC Irvine"}', (-117.841132, 33.643831), color='red')
    ax.annotate(f'△ {"CityLine, TX"}', (-96.697442, 32.999553), color='red')
    ax.set(xlabel='longitude', ylabel='latitude')
    ax.grid()


def updateOrbit(x: [float], y: [float], z: [float], h: [float]) -> None:
    pyplot.figure(2)
    pyplot.axes(projection='3d', xlabel='x (km)', ylabel='y (km)', zlabel='z (km)')
    pyplot.plot(x, y, z, 'red')
    pyplot.title("Geocentric Flight Path")

    pyplot.figure(3)
    pyplot.axes(xlabel='time (sec)', ylabel='altitude (km)')
    pyplot.plot(h, 'blue')
    pyplot.title("Flight Altitude")
    pyplot.grid()


duration = 1 * 3600
resolution = 1.0

tle = satnogs_calc.loadTLE()
response = satnogs_calc.getTLELineResponse(tle, "amicalsat")
lat, long, start, t = satnogs_calc.getLatLongPath(response, duration, resolution)
x, y, z, h = satnogs_calc.getOrbitPath(response, duration, resolution)
updatePath(lat, long, start, t)
updateOrbit(x, y, z, h)
pyplot.show()
