def satelliteFilter(satelliteList: [dict], mode: str = "AFSK", baud: int = 1200) -> [dict]:
    # filter the list of satellite by modulation mode and baud rate
    return [sat for sat in satelliteList if sat["mode"] is not None and mode in sat["mode"]
            and sat["baud"] is not None and baud == sat["baud"]]


def sortMostRecent(satelliteList: [dict], recent: bool = True) -> [dict]:
    # sort the list of satellite by timestamp (last known communication)
    return sorted(satelliteList, key=lambda x: x["time"], reverse=recent)
