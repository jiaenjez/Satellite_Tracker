from matplotlib import pyplot, animation
from matplotlib.animation import FuncAnimation
from skyfield.api import load

from src import satnogs_calc
import time


DURATION = 3 * 3600  # 3600 sec
RESOLUTION = 1/60  # r = 0.25 means 4 updates per minute
ANIMATION_SPEED = RESOLUTION * 60.0 * 1000  # set this to 3600 for more realistic speed
# ANIMATION_SPEED = 1


def updatePath(lat: [float], long: [float], start: (float, float), timestamp) -> FuncAnimation:
    timer = time.perf_counter()
    fig, ax = pyplot.subplots(figsize=(30, 10))
    ax.set_xlim([-270, 270])
    ax.set_ylim([-120, 120])
    ax.plot(long, lat, 'black')
    # ax.annotate(f'▀█▀ {start[0]:.4f}, {start[1]:.4f} @ {timestamp.utc_strftime()}', start, color='red')
    # ax.annotate(f'▀█▀ @ {timestamp.utc_strftime()}', start, color='red')
    ax.annotate(f'△ {"UC Irvine"}', (-117.841132, 33.643831), color='red')
    ax.annotate(f'△ {"Plano, TX"}', (-96.697442, 32.999553), color='red')
    ax.annotate(f'△ {"Anchorage, AK"}', (-149.9003, 61.2181), color='red')
    ax.annotate(f'△ {"NYC, NY"}', (-74.0060, 40.7128), color='red')
    ax.annotate(f'△ {"London, UK"}', (0.1278, 51.5074), color='red')
    ax.annotate(f'△ {"Dalian, China"}', (121.6147, 38.9140), color='red')
    ax.annotate(f'△ {"New Delhi, India"}', (77.2090, 28.6139), color='red')
    ax.annotate(f'△ {"Singapore"}', (103.8198, 1.3521), color='red')
    ax.annotate(f'△ {"Sydney, Australia"}', (-151.2093, -33.8688), color='red')
    ax.annotate(f'△ {"Johannesburg, South Africa"}', (28.0473, -26.2041), color='red')
    ax.annotate(f'△ {"Abu Dhabi, UAE"}', (54.3773, 24.4539), color='red')
    ax.annotate(f'△ {"Antarctica"}', (135, -82.8628), color='red')
    ax.annotate(f'△ {"Antarctica"}', (-135, -82.8628), color='red')
    ax.set(xlabel='longitude', ylabel='latitude', title='AMICALSAT')
    ax.grid()

    print(f'pyplot took {time.perf_counter() - timer:.3f} second to process')
    ts = load.timescale()

    def init():
        annot = ax.annotate(f'▀█▀ @ {ts.now().utc_strftime()}', (long[0], lat[0]), color='black')
        return annot,

    def update(frame):
        annot = ax.annotate(f'▀█▀ @ {ts.now().utc_strftime()}', (long[frame + 1], lat[frame + 1]), color='black')
        return annot,

    return animation.FuncAnimation(fig, update, frames=len(lat)-1, init_func=init, interval=ANIMATION_SPEED, blit=True)


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


tle = satnogs_calc.loadTLE()
response = satnogs_calc.getTLELineResponse(tle, "amicalsat")
lat, long, start, t, name = satnogs_calc.getLatLongPath(response, DURATION, RESOLUTION)
# x, y, z, h = satnogs_calc.getOrbitPath(response, DURATION, RESOLUTION)
var = updatePath(lat, long, start, t)  # DO NOT REMOVE THIS ASSIGNMENT, other gets garbage collected
pyplot.show()
