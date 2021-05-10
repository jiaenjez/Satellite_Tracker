import requests  # json

API_KEY = "36ff1b885dafa497e93073092cdac1c9887e510c"
TRANSMITTER_URL = "https://db.satnogs.org/api/transmitters/?key=36ff1b885dafa497e93073092cdac1c9887e510c&format=json"
SATELLITE_URL = "https://db.satnogs.org/api/satellites/?key=36ff1b885dafa497e93073092cdac1c9887e510c&format=json"
TLE_URL = "https://db.satnogs.org/api/tle/?key=36ff1b885dafa497e93073092cdac1c9887e510c&format=json"
TELEMETRY_URL = ""

CELESTRAK_URL = "https://www.celestrak.com/satcat/tle.php?CATNR=46287"


def getID() -> set:
    return {sat["norad_cat_id"] for sat in requests.get(SATELLITE_URL).json()}


def getSatellites() -> [dict]:
    transmitters = requests.get(TRANSMITTER_URL).json()
    satellites = requests.get(SATELLITE_URL).json()
    sat = {}
    for x in satellites:
        sat[x["norad_cat_id"]] = x["name"]  # Get satellite name from DB
    Satellites = []
    for x in transmitters:  # Use Transmitter uuid to make looking up satellite from job easier
        if x["alive"]:
            Satellites.append({"name": sat[x["norad_cat_id"]], "description": x["description"],
                               "norad_cat_id": x["norad_cat_id"],
                               "service": x["service"], "mode": x["mode"],
                               "baud": x["baud"], "time": x["updated"]})
    return Satellites


# def getTLE() -> dict:
#     pass
