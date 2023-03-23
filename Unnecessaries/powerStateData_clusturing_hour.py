import module as mod

import numpy as np
import pandas as pd
import glob
import os


directory = "E:/BeiweData/"
px_List = [f.name for f in os.scandir(directory) if f.is_dir()]
index = 0
check = False
proportions  = []
frequencies = []

path0 = glob.glob("E:/BeiweData/*")
for file0 in path0 :
# into each participant's power_state data

    file_count = len(file0)
    if file_count > 0 :
        
        duration_hour_arr = []
        frequency_hour_arr = []
        hour_name_arr = []
        participant_arr = []
        i=0

        path = glob.glob(file0+"/power_state/*"+".csv")       
        for file in path :
        # into participant's power_state data of each day hour
            hour_file_name = file.split("/power_state\\")[1]
            print(hour_file_name)
            i+=1

            duration = 0
            frequency = 0
            timestampX = -999

            data = pd.read_csv(file)
            data = data.to_numpy()

            times = data[:,1]
            events = data[:,2]

            power_state_data_hour = np.vstack((times,events)).T

            for data_row in power_state_data_hour:
                
                time = np.fromstring(data_row[0].split("T")[1], dtype=float, sep=':')
                timestamp = time[0]*3600 + time[1]*60 + time[2]

                if(time[0]>18 and time[0]<24):
                    if(data_row[1] == "Screen turned off" and timestampX != -999):
                        duration += timestamp-timestampX
                    elif(data_row[1] == "Screen turned on"):
                        timestampX = timestamp
                        frequency += 1

            duration_hour_arr.append(duration)
            frequency_hour_arr.append(frequency)
            hour_name_arr.append(hour_file_name)
            participant_arr.append(file.split("/BeiweData\\")[1].split(hour_file_name)[0])
        mod.append_data_in_csvFile(np.vstack((participant_arr,hour_name_arr,duration_hour_arr,frequency_hour_arr)).T, 
            'powerStateData_persons_hours.csv')
    else:
        px_List.pop(index)
        index -= 1

    print(index)
    index += 1

whole_data = pd.read_csv("powerStateData_persons_hours.csv")
whole_data = whole_data.to_numpy()
proportions = whole_data[:,2]
frequencies = whole_data[:,3]
clusters = mod.get_clustered_data(np.vstack((proportions, frequencies)),
    ['proportion','frequency'])

















