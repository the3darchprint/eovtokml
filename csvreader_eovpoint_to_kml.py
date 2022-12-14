import csv
import requests
import simplekml
import easygui

def fromcsvtokml():

    kml=simplekml.Kml()

    file = easygui.fileopenbox(filetypes=["*.csv"])
    fileoutput = easygui.filesavebox(default="csv_export.kml", filetypes=["*.kml"])

    f = open(file, mode="r")
    reader = csv.reader(f, delimiter=";")

    coords_from_csv = []

    for row in reader:
        # koords.append(row)
        coords_from_csv.append([str(row[0]), int(row[1]), int(row[2])])

    wgscoords_from_coords = []

    for i in coords_from_csv:
        pointname = i[0]
        ycoord = i[1]
        xcoord = i[2]
        get_coords_from_bme = str(f"http://www.agt.bme.hu/on_line/etrs2eov/etrs2eov.php?e={ycoord}&n={xcoord}&sfradio=single&format=TXT")
        coords = requests.get(get_coords_from_bme)
        coordstext = str(coords.text)
        wgslist = coordstext.split()
        wgs84y = wgslist[2]
        wgs84x = wgslist[1]
        wgscoords_from_coords.append([pointname, wgs84y, wgs84x])

    for row in wgscoords_from_coords:
        kml.newpoint(name=row[0], coords=[(row[2], row[1])])

    kml.save(fileoutput)





