import xml.dom.minidom
import os
import glob
import pandas as pd
import numpy as np
import time
import datetime

path = "/home/vinh/Downloads/final_work"
#set working directory
os.chdir(path)

filename_of_kml_file  = "/home/vinh/Downloads/final_work/checkin_tky.kml"

#find all csv files in the folder
#use glob pattern matching -> extension = 'csv'
#save result in list -> all_filenames
extension = 'csv'

#creating a list of csv file destination
#looking for the adress where the CSV file is stored
tokyo_checkin = glob.glob(path + "/dataset/dataset_TSMC2014_TKY." + extension, recursive=True)

#creating dataframe from csv files
for f in tokyo_checkin:
    tokyo_frame = pd.read_csv(f) 
#print(tokyo_frame)

df1 = tokyo_frame.loc[:,['latitude', 'longitude', 'utcTimestamp']] #selects 3 columns 
df1.reset_index(drop=True, inplace=True)
df1 = df1[['utcTimestamp', 'latitude', 'longitude']] #rearrange columns position
#print(df1)

#generate a final dataframe and save it at path.
df1.to_csv("final_frame_tokyo", index=False, encoding='utf-8-sig')

#Function to generate KML file
def processChild(node):
    # do some checks on node
    for child in node.childNodes:
        processChild(child)

def create_google_kml_override_map(list_of_locations):
    """Converts the override location to a KML file for exporting
    Refer to https://developers.google.com/kml/articles/geocodingforkml    
    Args: list_of_locations (list of coordinate pair): A list of all locations    
    Returns: xml.dom.minidom.Document(): A KML document
    """
    kmlDoc = xml.dom.minidom.Document()
    kmlRootElement = kmlDoc.createElementNS("http://earth.google.com/kml/2.2", "kml")

    kmlRootElement.setAttributeNS("", "xmlns", "http://www.opengis.net/kml/2.2")
    kmlRootElement.setAttributeNS("xmls", "xmlns:gx", "http://www.google.com/kml/ext/2.2")

    kmlRootElement = kmlDoc.appendChild(kmlRootElement)
    documentElement = kmlDoc.createElement("Document")
    documentElement = kmlRootElement.appendChild(documentElement)    


    folderElement= kmlDoc.createElement("Folder")

    nameElement = kmlDoc.createElement("name")
    textElement = kmlDoc.createTextNode("Check-in")
    nameElement.appendChild(textElement)
    folderElement.appendChild(nameElement)#Add name to folder in google earth
    
    for location in list_of_locations:

        # Point tag and its children #
        latitude = location[1]
        longitude = location[2]
        #timeStamp = location [0]
        #type(latitude)
        #type(longitude)

        if (not (np.isnan(latitude))) and (not np.isnan(longitude)) and latitude != 0  and longitude != 0: 
            iconStyleElement = kmlDoc.createElement("IconStyle")
            styleElement = kmlDoc.createElement("Style")
            iconElement = kmlDoc.createElement("Icon")
            hrefElement = kmlDoc.createElement("href")
            pointElement = kmlDoc.createElement("Point")
            coorElement = kmlDoc.createElement("coordinates")    
            #timeStampElement = kmlDoc.createElement("gx:TimeStamp")   #TimeStamp 

            #adding coordinates
            coordinates = f"{longitude},{latitude},0"
            coorElement.appendChild(kmlDoc.createTextNode(coordinates))
            pointElement.appendChild(coorElement)

            #whenElementAbove2 = kmlDoc.createElement("when")
            #strtimeStampAbove2 = f"{timeStamp}"
            #whenElementAbove2.appendChild(kmlDoc.createTextNode(strtimeStampAbove2))
            #timeStampElement.appendChild(whenElementAbove2)

            placemarkElement = kmlDoc.createElement("Placemark")
            colorElement = kmlDoc.createElement("color")
            scaleElement = kmlDoc.createElement("scale")


            iconStyleElement.appendChild(colorElement)
            iconStyleElement.appendChild(scaleElement)

            #color of icon
            # colors to be set this way : aabbggrr #
            color = "ff0000FF" #red
            strColor= color
            colorText = kmlDoc.createTextNode(strColor)
            colorElement.appendChild(colorText)

            #choosing the scale for icon
            strscaleElement = "0.5" 
            scaleText = kmlDoc.createTextNode(strscaleElement)
            scaleElement.appendChild(scaleText)

            #choosing favourite icon shape
            hrefText = kmlDoc.createTextNode("http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png")
            hrefElement.appendChild(hrefText)
            styleElement.appendChild(iconStyleElement)
                

            # Style tag and its children #
            iconStyleElement.appendChild(iconElement)
            iconElement.appendChild(hrefElement) 


            placemarkElement.appendChild(pointElement)
            placemarkElement.appendChild(styleElement)
                

            processChild(placemarkElement)


            folderElement.appendChild(placemarkElement)

      
    documentElement.appendChild(folderElement)
    
    return kmlDoc

#listCol is list_of_location
listCol = df1.values.tolist()
#print(listCol)

kml = create_google_kml_override_map(listCol)
with open(filename_of_kml_file, "w") as fp:
    fp.write(kml.toprettyxml(" "))
