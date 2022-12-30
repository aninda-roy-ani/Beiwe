#%%matplotlib inline
print( " " )

import numpy as np

import glob
import os

import pandas as pd
import csv


def save_data_in_csvFile( fields, data, filename ):

    with open( filename, 'w' ) as csvfile :
        csvwriter = csv.writer(csvfile) 
            
        csvwriter.writerow(fields) 
        csvwriter.writerows(data)
        

def standard_deviation( anyArr ):

    meanVal = np.mean(anyArr)
    anyArrValSum = 0.0

    for val in anyArr :
        anyArrValSum += pow((val-meanVal),2)

    return pow((anyArrValSum/anyArr.size),0.5)

directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

ind = 0

path0 = glob.glob("E:/BeiweData/*")
for file0 in path0 :
# into each participant's data (gps)

    file_count = len(file0)
    if file_count > 0 :

        latitudeSD = []
        longitudeSD = []
        altitudeSD = []
        dates = []
        
        latitude = np.array([])
        longitude = np.array([])
        altitude = np.array([])

        i = 0
        flag = False
        dateX = -365
        monthX = -12

        path = glob.glob(file0+"/gps/*"+".csv")       
        for file in path :
        # into participant's gps data of each day hour
        
            if flag == False :                      
                dateX = path[0].split("2022-")[1].split(" ")[0].split("-")[1]
                monthX = path[0].split("2022-")[1].split(" ")[0].split("-")[0]
                flag = True
            date = file.split("2022-")[1].split(" ")[0].split("-")[1]
            month = file.split("2022-")[1].split(" ")[0].split("-")[0]
            
            print(date)
            if(date != dateX):
                
                dates.append("2022-" + str(monthX) + "-" + str(dateX))
                
                if altitude.size > 0 and latitude.size > 0 and longitude.size > 0 :
                    latitudeSD.append(standard_deviation(latitude))
                    longitudeSD.append(standard_deviation(longitude))
                    altitudeSD.append(standard_deviation(altitude))
                
                latitude = np.array([])
                longitude = np.array([])
                altitude = np.array([])

            data = pd.read_csv(file)
            data = data.to_numpy()
            
            latitude = np.append(latitude, data[:,2])
            longitude = np.append(longitude, data[:,3])
            altitude = np.append(altitude, data[:,4])
            
            i += 1
            dateX = date
            monthX = month
            


        if(i==0):
            px_List.pop(ind)
            ind -= 1
        else:
            dates.append("2022-" + str(monthX) + "-" + str(dateX))
            
            latitudeSD.append(standard_deviation(latitude))
            longitudeSD.append(standard_deviation(longitude))
            altitudeSD.append(standard_deviation(altitude))
            
            print(dates)
            print(longitudeSD)
            
            filename = "gps_standard_deviation/" + px_List[ind] + ".csv"
            print(filename)
            save_data_in_csvFile(['Date','longitudeSD','latitudeSD','altitudeSD'], 
            np.vstack((dates, latitudeSD ,longitudeSD, altitudeSD)).T, filename)
            
        ind += 1

    

        

        

        

            



