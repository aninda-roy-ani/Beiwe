import numpy as np
import scipy as sp
import pandas as pd
import csv
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score




def standard_deviation( anyArr ):

    meanVal = np.mean(anyArr)
    anyArrValSum = 0.0

    for val in anyArr :
        anyArrValSum += pow((val-meanVal),2)

    return pow((anyArrValSum/anyArr.size),0.5)

        
def append_data_in_csvFile( data, filename ):
    
    with open( filename, 'a' ) as csvfile :
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows(data)



def getDataFrame(data, fields):
    return (pd.DataFrame(data, np.array(fields))).T


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
    
    if (scores == []):
        return 1
    return scores.index(max(scores)) + start_limit


def KMeansClustering( dataFrame,n ):
    
    X = dataFrame.to_numpy()
    #n = number_of_clusters(dataFrame)

    kmeans = KMeans(n_clusters=n)

    kmeans = kmeans.fit(X)
    labels = kmeans.predict(X)
    centroids = kmeans.cluster_centers_  #unused because of No Graphical Representation
    
    return labels
    
        
def get_clustered_data( data, fields ):
    
    dataframe = getDataFrame(data, fields)
    n = number_of_clusters(dataframe)
    labels = KMeansClustering(dataframe,n)
    
    #clusterData = clusterData + [clusters[i]+'\n' for i in range(n)]
    
    return labels