from matplotlib import pyplot, animation
from src import satnogs_calc

ANIMATION_SPEED = 1  # set this to 3600 for more realistic speed


def updatePath(lat: [float], long: [float], start: (float, float), timestamp) -> None:
    fig, ax = pyplot.subplots(figsize=(20, 10))
    ax.plot(long, lat, 'black')
    ax.annotate(f'▀█▀ {start[0]:.4f}, {start[1]:.4f} @ {timestamp.utc_strftime()}', start, color='red')
    ax.annotate(f'△ {"UC Irvine"}', (-117.841132, 33.643831), color='red')
    ax.annotate(f'△ {"Plano, TX"}', (-96.697442, 32.999553), color='red')
    ax.annotate(f'△ {"NYC, NY"}', (-74.0060, 40.7128), color='red')
    ax.annotate(f'△ {"London, UK"}', (0.1278, 51.5074), color='red')
    ax.annotate(f'△ {"Beijing, CHN"}', (116.4074, 39.9042), color='red')
    ax.annotate(f'△ {"Singapore"}', (103.8198, 1.3521), color='red')
    ax.annotate(f'△ {"Sydney, AUS"}', (-151.2093, -33.8688), color='red')
    ax.annotate(f'△ {"Johannesburg, SA"}', (28.0473, -26.2041), color='red')
    ax.annotate(f'△ {"Antarctica"}', (135, -82.8628), color='red')
    ax.annotate(f'△ {"Antarctica"}', (-135, -82.8628), color='red')
    ax.set(xlabel='longitude', ylabel='latitude', title='AMICALSAT')
    ax.grid()

    def init():
        annot = ax.annotate(f'▀█▀', (long[0], lat[0]), color='black')
        return annot,

    def update(frame):
        annot = ax.annotate(f'▀█▀', (long[frame], lat[frame]), color='black')
        return annot,

    return animation.FuncAnimation(fig, update, frames=len(lat), init_func=init, interval=ANIMATION_SPEED, blit=True)


def updateOrbit(x: [float], y: [float], z: [float], h: [float]) -> None:
    pyplot.figure(2)
    pyplot.axes(projection='3d', xlabel='x (km)', ylabel='y (km)', zlabel='z (km)')
    pyplot.plot(x, y, z, 'red')
    pyplot.title("Geocentric Flight Path")

    pyplot.figure(3)
    pyplot.axes(xlabel='time (min)', ylabel='altitude (km)')
    pyplot.plot(h, 'blue')
    pyplot.title("Flight Altitude")
    pyplot.grid()


duration = 5 * 3600
resolution = 0.25

tle = satnogs_calc.loadTLE()
response = satnogs_calc.getTLELineResponse(tle, "amicalsat")
lat, long, start, t = satnogs_calc.getLatLongPath(response, duration, resolution)
x, y, z, h = satnogs_calc.getOrbitPath(response, duration, resolution)
var = updatePath(lat, long, start, t)  # DO NOT REMOVE THIS ASSIGNMENT, other gets garbage collected
pyplot.show()
