from src import satnogs_api, satnogs_selection
import openpyxl  # excel
from datetime import datetime


def newWorkbook() -> openpyxl.Workbook:
    return openpyxl.Workbook()


def newTab(wb: openpyxl.Workbook, tabName: str, tabIndex: int = 0) -> openpyxl.Workbook.worksheets:
    return wb.create_sheet(tabName, tabIndex)


def addHeader(ws: openpyxl.Workbook.worksheets) -> None:
    ws["A1"] = "Name"
    ws["B1"] = "Description"
    ws["C1"] = "Norad_cat_id"
    ws["D1"] = "Service"
    ws["E1"] = "Mode"
    ws["F1"] = "Baud Rate"
    ws["G1"] = "Timestamp"


def saveFile(wb: openpyxl.Workbook, dir: str) -> None:
    wb.save(dir)


def export(result: [dict], dir: str) -> None:
    if not result:  # if list is empty
        return

    wb = newWorkbook()  # create a openpyxl WB object
    ws = newTab(wb, "allSatellite", 0)  # raw output
    addHeader(ws)

    for r in range(2, len(result) + 2):
        entry = result[r - 2]

        ws.cell(r, 1, entry["name"])
        ws.cell(r, 2, entry["description"])
        ws.cell(r, 3, entry["norad_cat_id"])
        ws.cell(r, 4, entry["service"])
        ws.cell(r, 5, entry["mode"])
        ws.cell(r, 6, entry["baud"])
        ws.cell(r, 7, entry["time"])

    # save to file
    saveFile(wb, dir)


# driver
allSatellite = satnogs_api.getSatellites()
filteredSatellite = satnogs_selection.satelliteFilter(allSatellite)
sortedSatellite = satnogs_selection.sortMostRecent(filteredSatellite)
export(allSatellite, 'D:\\satnogs_satellites.xlsx')
for v in sortedSatellite:
    print(v, end="\n")
