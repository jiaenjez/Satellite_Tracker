from matplotlib import pyplot, animation
from matplotlib.animation import FuncAnimation
from skyfield.api import load
from src import satnogs_calc, flightPath, satnogs_export
import time

DURATION = 3 * 3600  # 3600 sec
RESOLUTION = 1 / 60  # r = 0.25 means 4 updates per minute
ANIMATION_SPEED = RESOLUTION * 60.0 * 1000  # set this to 3600 for more realistic speed


def singleFlightPath(lat: [float], long: [float], start: (float, float), timestamp) -> FuncAnimation:
    timer = time.perf_counter()
    fig, ax = pyplot.subplots(figsize=(30, 10))
    ax.set_xlim([-270, 270])
    ax.set_ylim([-120, 120])
    ax.plot(long, lat, 'black')
    # ax.annotate(f'▀█▀ {start[0]:.4f}, {start[1]:.4f} @ {timestamp.utc_strftime()}', start, color='red')
    # ax.annotate(f'▀█▀ @ {timestamp.utc_strftime()}', start, color='red')
    ax.annotate(f'. {"UC Irvine"}', (-117.841132, 33.643831), color='red')
    ax.annotate(f'. {"Plano, TX"}', (-96.697442, 32.999553), color='red')
    ax.annotate(f'. {"Anchorage, AK"}', (-149.9003, 61.2181), color='red')
    ax.annotate(f'. {"NYC, NY"}', (-74.0060, 40.7128), color='red')
    ax.annotate(f'. {"London, UK"}', (0.1278, 51.5074), color='red')
    ax.annotate(f'. {"Dalian, China"}', (121.6147, 38.9140), color='red')
    ax.annotate(f'. {"Singapore"}', (103.8198, 1.3521), color='red')
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

    return animation.FuncAnimation(fig, update, frames=len(lat) - 1, init_func=init, interval=ANIMATION_SPEED,
                                   blit=True)


def getAllFlightPath():
    file = satnogs_export.loadTLE(satnogs_export.TLE_DIR)
    sats = []
    count = 0
    for r in file:
        satellite = flightPath.flightPath(r['tle0'], r['tle1'], r['tle2'], 10.0 * 3600, 3)
        print(count + 1, "/", len(file))
        count += 1
        satellite.findHorizonPath(satellite.findHorizonTime())
        sats.append(satellite)

    return sats


def plotAllFlightPath(allPath: []) -> FuncAnimation:
    fig, ax = pyplot.subplots(figsize=(20, 10))
    img = pyplot.imread("https://upload.wikimedia.org/wikipedia/commons/8/83/Equirectangular_projection_SW.jpg",
                        format='jpg')

    def setup():
        ax.set_xlim([-180, 180])
        ax.set_ylim([-90, 90])
        ax.imshow(img, origin='upper', extent=[-180, 180, -90, 90], alpha=0.75)
        ax.annotate(f'. {"UC Irvine"}', (-117.841132, 33.643831), color='black')
        ax.annotate(f'. {"Plano, TX"}', (-96.697442, 32.999553), color='black')
        ax.annotate(f'. {"Anchorage, AK"}', (-149.9003, 61.2181), color='black')
        ax.annotate(f'. {"NYC, NY"}', (-74.0060, 40.7128), color='black')
        ax.annotate(f'. {"London, UK"}', (0.1278, 51.5074), color='black')
        ax.annotate(f'. {"Dalian, China"}', (121.6147, 38.9140), color='black')
        ax.annotate(f'. {"Singapore"}', (103.8198, 1.3521), color='black')
        ax.annotate(f'. {"Johannesburg, South Africa"}', (28.0473, -26.2041), color='black')
        ax.set(xlabel='longitude', ylabel='latitude', title='NAME')
        # ax.grid()

    def init():
        setup()
        ax.set(xlabel='longitude', ylabel='latitude', title=allPath[0].name)
        long = allPath[0].path[1]
        lat = allPath[0].path[0]
        currPath = ax.plot(long, lat, 'black', label='ground track', linewidth=2)
        ax.legend(loc='upper right')
        return currPath,

    def update(frame):
        ax.cla()
        setup()
        ax.set(xlabel='longitude', ylabel='latitude', title=allPath[frame + 1].name)
        long = allPath[frame + 1].path[1]
        lat = allPath[frame + 1].path[0]
        currPath = ax.plot(long, lat, 'black', label='ground track', linewidth=2)
        ax.legend(loc='upper right')
        return currPath,

    return animation.FuncAnimation(fig, update, frames=len(allPath) - 1, init_func=init, interval=1000)


def plotAllRadioPass(sats: []):
    fig, ax = pyplot.subplots(figsize=(20, 10))
    img = pyplot.imread("https://upload.wikimedia.org/wikipedia/commons/8/83/Equirectangular_projection_SW.jpg",
                        format='jpg')

    def setup():
        ax.set_xlim([-180, 180])
        ax.set_ylim([-90, 90])
        ax.imshow(img, origin='upper', extent=[-180, 180, -90, 90], alpha=0.75)
        ax.annotate(f'. {"UC Irvine"}', (-117.841132, 33.643831), color='black')
        ax.annotate(f'. {"Plano, TX"}', (-96.697442, 32.999553), color='black')
        ax.annotate(f'. {"Anchorage, AK"}', (-149.9003, 61.2181), color='black')
        ax.annotate(f'. {"NYC, NY"}', (-74.0060, 40.7128), color='black')
        ax.annotate(f'. {"London, UK"}', (0.1278, 51.5074), color='black')
        ax.annotate(f'. {"Dalian, China"}', (121.6147, 38.9140), color='black')
        ax.annotate(f'. {"Singapore"}', (103.8198, 1.3521), color='black')
        ax.annotate(f'. {"Johannesburg, South Africa"}', (28.0473, -26.2041), color='black')
        ax.set(xlabel='longitude', ylabel='latitude', title='NAME')
        # ax.grid()

    def init():
        setup()
        ax.set(xlabel='longitude', ylabel='latitude', title=sats[0].name)
        sat = sats[0]
        currPath = None
        for p in sat.radioPass:
            long = p[1]
            lat = p[0]
            interval = p[3]
            t0 = interval[0].utc_strftime("%Y %b %d %H:%M:%S")
            t1 = interval[-1].utc_strftime("%H:%M:%S")
            currPath = ax.plot(long, lat, 'black', label=f'{t0} - {t1}, Duration:{len(interval)}', linewidth=2)
        if sat.radioPass:
            ax.legend(loc='upper right')
        return currPath,

    def update(frame):
        ax.cla()
        setup()
        ax.set(xlabel='longitude', ylabel='latitude', title=sats[frame + 1].name)
        sat = sats[frame + 1]
        currPath = None
        for p in sat.radioPass:
            long = p[1]
            lat = p[0]
            interval = p[3]
            t0 = interval[0].utc_strftime("%Y %b %d %H:%M:%S")
            t1 = interval[-1].utc_strftime("%H:%M:%S")
            currPath = ax.plot(long, lat, 'black', label=f'T: {t0} - {t1}, Duration:{len(interval)}', linewidth=2)
        if sat.radioPass:
            ax.legend(loc='upper right')
        return currPath,

    return animation.FuncAnimation(fig, update, frames=len(sats) - 1, init_func=init, interval=1000)


# tle = satnogs_export.loadTLE()
# response = satnogs_calc.getTLELineResponse(tle, "amicalsat")
# lat, long, start, t, name = satnogs_calc.getLatLongPath(response, DURATION, RESOLUTION)
# x, y, z, h = satnogs_calc.getOrbitPath(response, DURATION, RESOLUTION)
# pyplot.show()

s = getAllFlightPath()
g = plotAllRadioPass(s)
f = plotAllFlightPath(s)
# f.save('D:\\path.gif', dpi=100)
pyplot.show()
