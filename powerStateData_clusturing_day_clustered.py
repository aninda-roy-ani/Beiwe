import module as mod

import numpy as np
import pandas as pd
import glob
import os

participant_list = []
date_list = []
duration_list = []
frequency_list = []

whole_data = pd.read_csv("Unnecessaries/powerStateData_persons_hours.csv")
whole_data = whole_data.to_numpy()
print("read done")
proportions = whole_data[:,2]
frequencies = whole_data[:,3]
participants = whole_data[:,0]
hours = whole_data[:,1]

duration_day = 0
frequency_day = 0
datex = hours[0].split(" ")[0].split("-")[2]
for i in range(len(participants)):
    date = hours[i].split(" ")[0].split("-")[2]
    if(date == datex):
        duration_day+=proportions[i]
        frequency_day+=frequencies[i]
    else:
        participant_list.append(participants[i-1].split("/")[0])
        date_list.append(hours[i-1].split(" ")[0])
        duration_list.append(duration_day)
        frequency_list.append(frequency_day)
        duration_day = 0
        frequency_day = 0
        datex = date
        i-=1

participant_list.append(participants[i-1].split("/")[0])
date_list.append(hours[i-1].split(" ")[0])
duration_list.append(duration_day)
frequency_list.append(frequency_day)
        

clusters = mod.get_clustered_data(np.vstack((duration_list,frequency_list)),
    ['proportion','frequency'])

mod.append_data_in_csvFile(np.vstack((['ParticipantID','Date','Duration','Frequency','Cluster No'])).T, 
        'powerStateData_persons_day_with_clusturing.csv')
mod.append_data_in_csvFile( np.vstack((participant_list, date_list, duration_list, frequency_list, 
        clusters)).T, 'powerStateData_persons_day_with_clusturing.csv')

















