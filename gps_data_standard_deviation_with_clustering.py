#%%matplotlib inline
print( " " )

import numpy as np

import glob
import os

import pandas as pd
import csv

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def create_with_data_in_csvFile( fields, data, filename ):

    with open( filename, 'w' ) as csvfile :
        csvwriter = csv.writer(csvfile) 
        
        csvwriter.writerow(fields)     
        csvwriter.writerows(data)
        
        
def append_data_in_csvFile( data, filename ):
    
    with open( filename, 'a' ) as csvfile :
        csvwriter = csv.writer(csvfile) 
            
        csvwriter.writerows(data)
        

def standard_deviation( anyArr ):

    meanVal = np.mean(anyArr)
    anyArrValSum = 0.0

    for val in anyArr :
        anyArrValSum += pow((val-meanVal),2)

    return pow((anyArrValSum/anyArr.size),0.5)


def getDataFrame(data):
    
    fields = ['latitude','longitude','altitude']
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
    
        
def get_clustered_gpsData( data ):
    
    dataframe = getDataFrame(data)
    n = number_of_clusters(dataframe)
    labels = KMeansClustering(dataframe,n)
    
    #clusterData = clusterData + [clusters[i]+'\n' for i in range(n)]
    
    return labels


#def groupingclusters():
    
        

directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

ind = 0

path0 = glob.glob("E:/BeiweData/*")
for file0 in path0 :
# into each participant's data (gps)

    file_count = len(file0)
    if file_count > 0 :

        timestamps = []
        latitudeSD = []
        longitudeSD = []
        altitudeSD = []
        dates = []
        
        timestamp = np.array([])
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
            
            #print(date)
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
            
            timestamp = np.append(timestamp, data[:,0])
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
            
            #print(dates)
            #print(longitudeSD)
            
            
            clusters = get_clustered_gpsData(np.vstack((latitudeSD ,longitudeSD, altitudeSD)))
            print(clusters)
            #filename = "gps_clustering_personDay/" + px_List[ind] + ".csv"
            print(px_List[ind])
            px_tempList = [px_List[ind]] * len(longitudeSD)
            
            if(('gps_data_SD_personDay.csv') == False ):
                create_with_data_in_csvFile(['Participant iD','Date','longitudeSD','latitudeSD','altitudeSD','cluster'], 
                    np.vstack((px_tempList, dates, latitudeSD ,longitudeSD, altitudeSD, clusters)).T, 
                    'gps_data_SD_personDay.csv')
            else:
                append_data_in_csvFile( np.vstack((px_tempList, dates, latitudeSD ,longitudeSD, altitudeSD, clusters)).T, 
                    'gps_data_SD_personDay.csv')
            
            
            
            
        ind += 1

    

        

        

        

            



