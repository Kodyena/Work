import numpy as np
import sys 
from shapely.geometry import shape, Point
import shapefile
import random 
import re
import xlsxwriter

#get location in uk
def random_country_point(shape_location, country_name):
    shapes = shapefile.Reader(shape_location)
    country = [s for s in shapes.records() if country_name in s][0]

    country_id = int(re.findall(r'\d+',str(country))[0])
    shape_records = shapes.shapeRecords()
    feature = shape_records[country_id].shape.__geo_interface__

    shape_geometry = shape(feature)
    minx, miny, maxx, maxy = shape_geometry.bounds

    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if shape_geometry.contains(p):
            return p.x, p.y

#setup data
n = int(sys.argv[1])
data = [None for x in range(n + 1) ]
column_names = ["Detector_ID", "Detector_Name", "Dectector_Location", "Dectector_Type", "Dectector_OEM", "Dectector_Battery_Percentage",
                 "Dectector_Signal_Strength", "Detector_Connectivity_Status", "Dectector_Temp"]
types = ["Gas-Filled", "Scintillators", "Solid State"]
oems = ["Manufacturer1", "Manufacturer2", "Manufacturer3"]
connectivities = ["Great", "Good", "OK", "Bad", "Disconnected"]
temp_range = [10, 70]

data[0] = column_names

#generate data
for i in range(n):
    id = i
    name = "Detector {}".format(i)
    lat, long = random_country_point("World_Countries.shp", "United Kingdom")
    type = types[random.randint(0, types.__len__() - 1)]
    oem = oems[random.randint(0, oems.__len__() - 1)]
    battery = random.randint(0, 100)
    signal_strength = random.randint(0, 100)
    connectivity = connectivities[random.randint(0, connectivities.__len__() - 1)]
    temp = random.randint(temp_range[0], temp_range[1])
    data[i + 1] = [str(i), 
            str(name), 
            "({},{})".format(lat, long),
            str(type),
            str(oem),
            str(battery),
            str(signal_strength),
            str(connectivity),
            str(temp)]
    
#write to excel
wb = xlsxwriter.Workbook("test_data.xlsx")
ws = wb.add_worksheet()
col = 0

for row, data in enumerate(data):
    ws.write_row(row, col, data)

wb.close()
