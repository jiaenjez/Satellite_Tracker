# add change

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
    sat = {s["norad_cat_id"]: s["name"] for s in requests.get(SATELLITE_URL).json()}

    return [{"name": sat[s["norad_cat_id"]], "description": s["description"],
             "norad_cat_id": s["norad_cat_id"],
             "service": s["service"], "mode": s["mode"],
             "baud": s["baud"], "time": s["updated"]}
            for s in requests.get(TRANSMITTER_URL).json() if s["alive"]]


def getTLE() -> [dict]:
    # get TLE response from api, TLE is used to calculate flight path

    return [tle for tle in requests.get(TLE_URL).json()]
