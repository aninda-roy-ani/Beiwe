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


dates = []
directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

path0 = glob.glob("E:/pyhton/psdTest/*")
for file0 in path0 :
# into each participant's data (gps)
    
    count = 0

    longitudeArray = []
    latitudeArray = []
    altitudeArray = []
    
    path = glob.glob(file0+"/gps/*"+".csv")
    for file in path :
    # into participant's gps data of each day hour
        
        count += 1
        flag = False
        

        data = pd.read_csv(file)
        data = data.to_numpy()
        
        date = file.split("2022-")[1].split(" ")[0].split("-")[1]
        month = file.split("2022-")[1].split(" ")[0].split("-")[0]
        
        
        
        dated = "2022-" + str(month) + "-" + str(date)
        print(dated)
        dates.append("2022-" + str(month) + "-" + str(date))

        print(date)
        
print(dates)