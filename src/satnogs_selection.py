def satelliteFilter(satelliteList: [dict], mode: str = "AFSK", baud: int = 1200) -> [dict]:
    filtered = []
    for sat in satelliteList:
        if sat["mode"] == mode and sat["baud"] == int(baud):
            # print(sat)
            filtered.append(sat)

    return filtered


def sortMostRecent(satelliteList: [dict], recent: bool = True) -> list:
    ret = sorted(satelliteList, key=lambda x: x["time"], reverse=recent)

    return ret
