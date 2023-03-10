import module as mod

import numpy as np
import pandas as pd
import glob
import os


directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]
index = 0
check = False
proportion  = []
frequency = []

path0 = glob.glob("E:/BeiweData/*")
for file0 in path0 :
# into each participant's power_state data

    file_count = len(file0)
    if file_count > 0 :

        numberOfDays = 0
        numberOfHours = 0
        screenOnCount = 0
        duration = 0
        flag = False
        dateX = -365
        timestampX = -999

        path = glob.glob(file0+"/power_state/*"+".csv")       
        for file in path :
        # into participant's power_state data of each day hour

            data = pd.read_csv(file)
            data = data.to_numpy()

            times = data[:,1]
            events = data[:,2]

            if flag == False :                      
                dateX = path[0].split("2022-")[1].split(" ")[0].split("-")[1]
                flag = True
            date = file.split("2022-")[1].split(" ")[0].split("-")[1]

            if (date != dateX):

                numberOfDays += 1
                timestampX = -999
                flag = True
            
            numberOfHours += 1

            power_state_data_hour = np.vstack((times,events)).T

            for data_row in power_state_data_hour:
                
                time = np.fromstring(data_row[0].split("T")[1], dtype=float, sep=':')
                timestamp = time[0]*3600 + time[1]*60 + time[2]

                if(time[0]>18 and time[0]<24):
                    if(data_row[1] == "Screen turned off" and timestampX != -999):
                        duration += timestamp-timestampX
                    elif(data_row[1] == "Screen turned on"):
                        timestampX = timestamp
                        screenOnCount += 1
            
            dateX = date
        
        if (numberOfDays == 0):
            px_List.pop(index)
            index -= 1
        else:
            numberOfDays += 1
            proportion.append(round(duration/numberOfHours, 5))
            frequency.append(round(screenOnCount/numberOfHours, 5))
    
    else:
        px_List.pop(index)
        index -= 1

    print(index)
    index += 1

clusters = mod.get_clustered_data(np.vstack((proportion, frequency)),
    ['proportion','frequency'])
        
if(check == False ):
    mod.append_data_in_csvFile(np.vstack((['ParticipantID','Time Proportion','Frequency','Cluster No'])).T, 
        'powerStateData_persons.csv')
mod.append_data_in_csvFile( np.vstack((px_List, proportion, frequency, clusters)).T, 
    'powerStateData_persons.csv')













