import ezdxf
import requests
import simplekml
import easygui 

def dxflinetokml():

    lines_kml=simplekml.Kml()

    #input output file browser
    fileinput = easygui.fileopenbox(filetypes=["*.dxf"])
    fileoutput = easygui.filesavebox(default="dxfexport.kml", filetypes=["*.kml"])
    dwg = ezdxf.readfile(fileinput)

    modelspace = dwg.modelspace()

    #polylines from dxf file into
    linelist = []
    for name, line in enumerate(modelspace.query('LWPOLYLINE'), start=1):
        with line.points() as points:
            for name, coords in enumerate(points):
                linelist.append([str(name), int(coords[0]), int(coords[1])])

    wgslist_from_linelist = []

    #request from bme to transformation coords
    for i in linelist:
        ycoord = i[1]
        xcoord = i[2]
        coords_from_url = str(f"http://www.agt.bme.hu/on_line/etrs2eov/etrs2eov.php?e={ycoord}&n={xcoord}&sfradio=single&format=TXT")
        coords = requests.get(coords_from_url)
        coordstext = str(coords.text)
        wgslist = coordstext.split()
        wgs84y = wgslist[1]
        wgs84x = wgslist[2]
        wgslist_from_linelist.append([wgs84y, wgs84x])

    lines_kml.newlinestring(
        name="line",
        description="line from dxf",
        coords=wgslist_from_linelist)

    lines_kml.save(fileoutput)
