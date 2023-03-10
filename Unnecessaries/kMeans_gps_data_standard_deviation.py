#%%matplotlib inline
print( " " )

import numpy as np

import glob
import os

import pandas as pd
import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def number_of_clusters( dataFrame ):
# deciding number of clusters using using silhouette score method

    scores = []
    start_limit = 2
    end_limit = int((dataFrame.shape[0]//2)**0.5) + 1

    for k in range(start_limit, end_limit):
        model = KMeans(n_clusters=k)
        model.fit(dataFrame)
        pred = model.predict(dataFrame)
        scores.append(silhouette_score(dataFrame, pred))

    return scores.index(max(scores)) + start_limit        


def save_data_in_csvFile( fields, data, filename ):

    with open( filename, 'w' ) as csvfile :
        csvwriter = csv.writer(csvfile) 
            
        csvwriter.writerow(fields) 
        csvwriter.writerows(data)


def dataFrame( column_to_drop, filename ):

    dataFrame = pd.read_csv(filename)
    dataFrame.drop(column_to_drop, axis=1, inplace=True)

    return dataFrame


def plot_3D_KMeansClustering( dataFrame ):

    X = dataFrame.to_numpy()
    n = number_of_clusters(dataFrame)

    kmeans = KMeans(n_clusters=n)

    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(centroids[:,0],centroids[:,1],centroids[:,2],c="black",s=80,label="Centers",alpha=1)
    colorArr = np.array( ["blue", "yellow", "red", "green", "cyan", "magenta"] )
    for i in range(n):
        x = np.array(labels == i)
        ax.scatter(X[x,0],X[x,1],X[x,2],c=colorArr[i],s=40,label="C"+str(i+1))

    ax.legend()
    plt.show()


def standard_deviation( anyArr ):

    meanVal = np.mean(anyArr)
    anyArrValSum = 0.0

    for val in anyArr :
        anyArrValSum += pow((val-meanVal),2)

    return pow((anyArrValSum/anyArr.size),0.5)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


index_px = 0

px_longitude_sdArr = []
px_latitude_sdArr = []
px_altitude_sdArr = []


directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

path0 = glob.glob("E:/BeiweData/*")
for file0 in path0 :
# into each participant's data (gps)
    
    count = 0

    longitudeArray = []
    latitudeArray = []
    altitudeArray = []
    
    path = glob.glob(file0+"/gps/*"+".csv")
    for file in path :
    # into participant's gps data of each day
        
        count += 1
        flag = False

        data = pd.read_csv(file)
        data = data.to_numpy()

        longitudeValueSum = 0.00
        latitudeValueSum = 0.00
        altitudeValueSum = 0.00

        latitudeValueX = -1
        longitudeValueX = -1
        altitudeValueX = -1

        timeValueX = -1

        for x in data :

            t = np.fromstring(x[1].split("T")[1], dtype=float, sep=':')
            timeValue = t[0]*3600.0 + t[1]*60.0 + t[2]

            latitudeValue = x[2]
            longitudeValue = x[3]
            altitudeValue = x[4]

            if flag :
                time_diff = timeValue-timeValueX

                if time_diff != 0 :
                    longitudeValueSum += (abs(longitudeValue-longitudeValueX)/time_diff)
                    latitudeValueSum += (abs(latitudeValue-latitudeValueX)/time_diff)
                    altitudeValueSum += (abs(altitudeValue-altitudeValueX)/time_diff)

                longitudeValueX = longitudeValue
                latitudeValueX = latitudeValue
                altitudeValueX = altitudeValue

                timeValueX = timeValue

            flag = True
        
        longitudeArray.append(longitudeValueSum)
        latitudeArray.append(latitudeValueSum)
        altitudeArray.append(altitudeValueSum)

    if count > 1 :
        px_longitude_sdArr.append(standard_deviation(np.asarray(longitudeArray)))
        px_latitude_sdArr.append(standard_deviation(np.asarray(latitudeArray)))
        px_altitude_sdArr.append(standard_deviation(np.asarray(altitudeArray)))
    else :
        px_List.pop(index_px)
        index_px -= 1

    index_px += 1



file_name = "gps_standard_deviation_eachParticipant.csv"

save_data_in_csvFile(['PARTICIPANTS','longitudeSD','latitudeSD','altitudeSD'], 
        np.vstack((px_List, px_longitude_sdArr, px_latitude_sdArr, px_altitude_sdArr)).T, file_name)

plot_3D_KMeansClustering(dataFrame('PARTICIPANTS', file_name))




    
# %%
