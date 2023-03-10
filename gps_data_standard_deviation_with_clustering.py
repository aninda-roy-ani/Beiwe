print( " " )
import module as mod

import numpy as np
import pandas as pd
import glob
import os

directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]

ind = 0
check = False

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
                    
                    latitudeSD.append(mod.standard_deviation(latitude))
                    longitudeSD.append(mod.standard_deviation(longitude))
                    altitudeSD.append(mod.standard_deviation(altitude))
                    
                
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
            
            latitudeSD.append(mod.standard_deviation(latitude))
            longitudeSD.append(mod.standard_deviation(longitude))
            altitudeSD.append(mod.standard_deviation(altitude))
            
            clusters = mod.get_clustered_data(np.vstack((latitudeSD ,longitudeSD, altitudeSD)),
                ['longitudeSD','latitudeSD','altitudeSD'])
            px_tempList = [px_List[ind]] * len(longitudeSD)
            
            if(check == False ):
                mod.append_data_in_csvFile(np.vstack((['ParticipantID','Date','Latitude','Longitude','Altitude','Cluster No'])).T, 
                    'gps_data_SD_personDay.csv')
                check = True
            
            mod.append_data_in_csvFile( np.vstack((px_tempList, dates, latitudeSD ,longitudeSD, altitudeSD, clusters)).T, 
                    'gps_data_SD_personDay.csv')
            
            
            
            
        ind += 1

    

        

        

        

            



