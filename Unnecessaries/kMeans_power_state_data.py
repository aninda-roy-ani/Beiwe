#%%matplotlib inline

import numpy as np
import pandas as pd
import glob
import csv
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

path = glob.glob("E:/BeiweData/*"+"/power_state/*"+".csv")
last_id = "xxx"
sum = 0.0
night_sum = 0.0
ps_array = []
ps_night_array = []
participants = []
i = 0
for file in path:
    data = pd.read_csv(file)
    participant_id = file.split("\\", 3)[1]
    #print(i)
    i += 1
    #print(participant_id)
    #arr = []
    #array = data.to_numpy()
    array1 = data.to_numpy()[:,1]
    array2 = data.to_numpy()[:,2]
    arrays = np.vstack((array1,array2)).T
    old_tstamp = -1.0
    for arr in arrays:
        #print(arr)
        event = arr[1]
        #print(event)
        time = arr[0].split("T")[1]
        #print(time)
        t = np.fromstring(time, dtype=float, sep=':')
        tstamp = t[0]*3600 + t[1]*60 + t[2]
        #print(tstamp)
        if participant_id==last_id:
            if event == "Screen turned off":
                if old_tstamp != -1.0:
                    sum += (tstamp - old_tstamp)/3600
                    if t[0]>=18.0:
                        if t[0]<=22.0:
                            night_sum += (tstamp - old_tstamp)/3600
            elif event == "Screen turned on":
                old_tstamp = tstamp
        else:
            participants.append(participant_id)
            if last_id != "xxx":
                old_tstamp = -1.0
                ps_array.append(sum)
                ps_night_array.append(night_sum)
                sum = 0.0
                night_sum = 0.0
            last_id = participant_id

ps_array.append(sum)
ps_night_array.append(night_sum)
print("Participants ID || Power State Data || Pawer State Night Data")
result = np.vstack((participants, ps_array, ps_night_array)).T
print(result)
#print(participants)
#print(ps_array)
#print(ps_night_array)

#plt.scatter(ps_array,ps_night_array)
#plt.show

coordinates = list(zip(ps_array, ps_night_array))

inertias = []

for i in range(1,11):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(coordinates)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,11), inertias, marker='o')
plt.title('Elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()


kmeans = KMeans(n_clusters=5)
kmeans.fit(coordinates)

plt.scatter(ps_array, ps_night_array, c=kmeans.labels_)
plt.show()

fields = ['Participants','PS Overall Data','PS Night Data']
filename = "powers_state_summery.csv"
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
        
    csvwriter.writerow(fields) 
    csvwriter.writerows(result)
    

# %%
