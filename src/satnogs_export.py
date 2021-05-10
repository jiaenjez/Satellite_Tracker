from src import satnogs_api, satnogs_selection
import openpyxl  # excel
from datetime import datetime

TABSNAME = {0: "allSatellite", 1: "filteredSatellite", 2: "sortedSatellite"}
DIR = 'D:\\satnogs_satellites.xlsx'


def newWorkbook() -> openpyxl.Workbook:
    # create a new openpyxl excel object
    return openpyxl.Workbook()


def newTab(wb: openpyxl.Workbook, tabName: str, tabIndex: int = 0) -> openpyxl.Workbook.worksheets:
    # create a new tab in excel
    return wb.create_sheet(tabName, tabIndex)


def addHeader(ws: openpyxl.Workbook.worksheets) -> None:
    # add these headers to row 1 of current excel tab
    ws["A1"] = "Name"
    ws["B1"] = "Description"
    ws["C1"] = "Norad_cat_id"
    ws["D1"] = "Service"
    ws["E1"] = "Mode"
    ws["F1"] = "Baud Rate"
    ws["G1"] = "Timestamp"


def exportData(ws: openpyxl.Workbook.worksheets, result: [dict]) -> None:
    for r in range(2, len(result) + 2):
        entry = result[r - 2]

        ws.cell(r, 1, entry["name"])
        ws.cell(r, 2, entry["description"])
        ws.cell(r, 3, entry["norad_cat_id"])
        ws.cell(r, 4, entry["service"])
        ws.cell(r, 5, entry["mode"])
        ws.cell(r, 6, entry["baud"])
        ws.cell(r, 7, entry["time"])


def saveFile(wb: openpyxl.Workbook, dir: str) -> None:
    # save openpyxl workbook to specified directory as an excel file
    wb.save(dir)


def exportTab(wb: openpyxl.Workbook, tab: int, result: [dict]) -> None:
    #  export data from dict to excel tab
    if not result:  # if list is empty, do nothing
        return

    ws = newTab(wb, TABSNAME[tab], tab)
    addHeader(ws)
    exportData(ws, result)


# driver
allSatellite = satnogs_api.getSatellites()
filteredSatellite = satnogs_selection.satelliteFilter(allSatellite)
sortedSatellite = satnogs_selection.sortMostRecent(filteredSatellite)
wb = newWorkbook()
exportTab(wb, 0, allSatellite)
exportTab(wb, 1, filteredSatellite)
exportTab(wb, 2, sortedSatellite)
saveFile(wb, DIR)
for v in sortedSatellite:
    print(v, end="\n")
