GOOGLE_API_KEY = ""  # Insert API key here
BING_API_KEY = ""  # Insert API key here


def getLocation() -> str:
    #  return input("Address: ")
    """

    :return: User Input of Address
    """
    return "University of California, Irvine"


def getLatLong(loc: str) -> (float, float):
    """

    :param loc: String representation of Observer's address
    :return: Pair of LatLong
    """
    pass


def bingGeocoding() -> (float, float):
    pass


def googleGeocoding() -> (float, float):
    pass
