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
    print(X)
    n = number_of_clusters(dataFrame)

    kmeans = KMeans(n_clusters=n)

    kmeans = kmeans.fit(X)
    print(kmeans)
    labels = kmeans.predict(X)
    print(labels)
    centroids = kmeans.cluster_centers_
    print(centroids)


def convert_arrayToString( labels,npArr,n ):
    clusterStringList = [''] * n
    for i in range(n) :
        clusterStringList[i].append()
        
        
    cstr = []


def standard_deviation( anyArr ):

    meanVal = np.mean(anyArr)
    anyArrValSum = 0.0

    for val in anyArr :
        anyArrValSum += pow((val-meanVal),2)

    return pow((anyArrValSum/anyArr.size),0.5)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

df = pd.DataFrame({'points': [18, 23, 19, 14, 14, 11, 20, 28, 30, 31,
                              35, 33, 29, 25, 25, 27, 29, 30, 19, 23],
                   'assists': [3, 3, 4, 5, 4, 7, 8, 7, 6, 9, 12, 14,
                               8, 9, 4, 3, 4, 12, 15, 11],
                   'rebounds': [15, 14, 14, 10, 8, 14, 13, 9, 5, 4,
                                11, 6, 5, 5, 3, 8, 12, 7, 6, 5]})

dt = np.array([[18,3,15],[23,3,14],[19,4,14],[14,5,10],[14,4,8],[11,7,14],[20,8,13],[28,7,9],[30,6,5],[31,9,4]])
    
dta = np.array([[18, 23, 19, 14, 14, 11, 20, 28, 30, 31, 35, 33, 29, 25, 25, 27, 29, 30, 19, 23],
              [3, 3, 4, 5, 4, 7, 8, 7, 6, 9, 12, 14, 8, 9, 4, 3, 4, 12, 15, 11],
              [15, 14, 14, 10, 8, 14, 13, 9, 5, 4, 11, 6, 5, 5, 3, 8, 12, 7, 6, 5]])

fields = ['long_night','lat_night','alt_night']
dfr = (pd.DataFrame(dta, np.array(fields))).T
print(dfr.head())
plot_3D_KMeansClustering(dfr)


                

