from src import satnogs_api, satnogs_selection, satnogs_calc, location_input
from skyfield.api import EarthSatellite, load
import requests


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
        if "amicalsat" in str(l["tle0"]).lower():
            line0 = l["tle0"]
            line1 = l["tle1"]
            line2 = l["tle2"]

    ts = load.timescale()
    t = ts.now()
    print(t.utc_strftime())

    return [line0, line1, line2]


def testGenerateSatellite(lines: [str, str, str]):
    satellite = EarthSatellite(lines[1], lines[2], lines[0], load.timescale())
    ts = load.timescale()
    xyz = []

    for minute in range(0, 20):
        t = ts.utc(2021, 5, 22, 10, minute, 0)  # how can I specify time in a better way than doing this???
        geocentric = satellite.at(t)
        xyz.append(geocentric.position.km)

    return xyz


response = testGetTLE()
xyz = testGenerateSatellite(response)
for l in xyz:
    print(l)
