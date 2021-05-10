def satelliteFilter(satelliteList: [dict], mode: str = "AFSK", baud: int = 1200) -> [dict]:
    # filter the list of satellite by modulation mode and baud rate
    return [sat for sat in satelliteList if sat["mode"] == mode and sat["baud"] == int(baud)]


def sortMostRecent(satelliteList: [dict], recent: bool = True) -> [dict]:
    # sort the list of satellite by timestamp (last known communication)
    return sorted(satelliteList, key=lambda x: x["time"], reverse=recent)
