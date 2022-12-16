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

directory = "E:/Beiwe Data/"
#directory = "E:/pyhton/psdTest/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

ind = 0

path0 = glob.glob("E:/Beiwe Data/*")
#path0 = glob.glob("E:/pyhton/psdTest/*")
for file0 in path0 :
# into each participant's data (gps)

    latitudeSD = []
    longitudeSD = []
    altitudeSD = []

    i = 0

    path = glob.glob(file0+"/gps/*"+".csv")
    for file in path :
    # into participant's gps data of each day
        i += 1

        data = pd.read_csv(file)
        data = data.to_numpy()

        latitude = data[:,2]
        longitude = data[:,3]
        altitude = data[:,4]

        latitudeSD.append(standard_deviation(latitude))
        longitudeSD.append(standard_deviation(longitude))
        altitudeSD.append(standard_deviation(altitude))

    if(i==0):
        px_List.pop(ind)
        ind -= 1
    else:
        filename = "gps_standard_deviation/" + px_List[ind] + ".csv"
        print(filename)
        save_data_in_csvFile(['longitudeSD','latitudeSD','altitudeSD'], 
        np.vstack((latitudeSD ,longitudeSD, altitudeSD)).T, filename)

    
    ind += 1

    

        

        

        

            



