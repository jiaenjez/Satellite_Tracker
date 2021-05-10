def satelliteFilter(satelliteList: [dict], mode: str = "AFSK", baud: int = 1200) -> [dict]:
    return [sat for sat in satelliteList if sat["mode"] == mode and sat["baud"] == int(baud)]


def sortMostRecent(satelliteList: [dict], recent: bool = True) -> [dict]:
    return sorted(satelliteList, key=lambda x: x["time"], reverse=recent)
