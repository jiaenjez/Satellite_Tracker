import requests  # json

GOOGLE_API_KEY = ""  # Insert API key here
BING_API_KEY = "AlG8wXq_mQ7kAhYeZzRQPsRPaFxei31_kBCmTW9P_RFOkhFBr1HCl9eT0NTkwEen"  # Insert API key here
BING_BASE_URL = "http://dev.virtualearth.net/REST/v1/Locations/US/{adminDistrict}/{postalCode}/{locality}/{" \
                "addressLine}?includeNeighborhood={includeNeighborhood}&include={includeValue}&maxResults={" \
                "maxResults}&key={BingMapsAPIKey}"


def getLocation() -> str:
    #  return input("Address: ")
    """

    :return: User Input of Address
    """
    temp = "University of California, Irvine"
    ret = str()

    for c in temp:
        if c == " ":
            ret += "%20"
        else:
            ret += c
    return ret


def getURL() -> str:
    adminDistrict = "CA"
    postalCode = "92697"
    locality = "Irvine"
    addressLine = getLocation()
    url = f'http://dev.virtualearth.net/REST/v1/Locations/US/{adminDistrict}/{postalCode}/{locality}/{addressLine}?o=json&key={BING_API_KEY}'

    return url


def getLatLong(loc: str) -> [float, float]:
    """

    :param loc: String representation of Observer's address
    :return: Pair of LatLong
    """

    adminDistrict = "CA"
    postalCode = "92697"
    locality = "Irvine"
    addressLine = getLocation()
    url = f'http://dev.virtualearth.net/REST/v1/Locations/US/{adminDistrict}/{postalCode}/{locality}/{addressLine}?o=json&key={BING_API_KEY}'
    response = requests.get(url).json()

    return response["resourceSets"][0]["resources"][0]["point"]["coordinates"]


def bingGeocoding() -> [float, float]:
    """

    :return:
    """
    pass


def googleGeocoding() -> (float, float):
    pass
