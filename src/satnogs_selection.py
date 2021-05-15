from src import satnogs_api


def satelliteFilter(satelliteList: [dict], mode: str = "AFSK", baud: int = 1200) -> [dict]:
    """
    filter the list of satellite by modulation mode and baud rate

    :param satelliteList: List of Satellite information from Satnogs
    :param mode: Modulation Type
    :param baud: Data Transfer Rate
    :return: List of Satellite information filtered
    """

    return [sat for sat in satelliteList if sat["mode"] is not None and mode in sat["mode"]
            and sat["baud"] is not None and baud == sat["baud"]]


def sortMostRecent(satelliteList: [dict], recent: bool = True) -> [dict]:
    """
    filter the list of satellite by modulation mode and baud rate

    :param satelliteList: List of Satellite information from Satnogs
    :param recent: True = Most recent first
    :return: List of Satellite information sorted
    """

    # sort the list of satellite by timestamp (last known communication)
    return [sat for sat in sorted(satelliteList, key=lambda x: x["time"], reverse=recent)
            if int(sat["time"][0:4]) >= 2018]


def getNoradID(satelliteList: [dict]) -> {str}:
    """
    get a set of NoradID from dict, using set to improve
    search performance from O(n) to O(1)

    :param satelliteList: List of Satellite information from Satnogs
    :return: Set of NoRadID in String format
    """

    return {sat["norad_cat_id"] for sat in satelliteList}


def tleFilter(satelliteList: [dict]) -> [dict]:
    """
    Push TLE information from Satnogs based on given NoRadID

    :param satelliteList: List of Satellite information from Satnogs
    :return: List of Satellite's TLE information from Satnogs
    """
    return [sat for sat in satnogs_api.getTLE() if sat["norad_cat_id"] in getNoradID(satelliteList)]
