#%%matplotlib inline

import numpy as np
import pandas as pd
import glob
import csv
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_swiss_roll
X, t = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

path0 = glob.glob("E:/pyhton/psd/*")
#path = glob.glob("E:/pyhton/psdTest/*"+"/gps/*"+".csv")
a1 = []
a2 = []
a3 = []
for f in path0:
    print(f)
    path = glob.glob(f+"/gps/*"+".csv")
    
    lats = 0.0
    lngs = 0.0
    alts = 0.0
    i = 0
    for file in path:
        #print(file)
        data = pd.read_csv(file)
        #print(data.to_numpy()[:,3])
        
        lat_x = 0.0
        lng_x = 0.0
        alt_x = 0.0
        t_x = 0.0
        for x in data.to_numpy():
            tl = np.fromstring(x[1].split("T")[1], dtype=float, sep=':')
            t = tl[0]*3600 + tl[1]*60 + tl[2]
            if t_x != 0:
                t_x
            if lat_x != 0:
                if t-t_x != 0:
                    i += 1
                    lngs += abs(x[2]-lng_x)/(t-t_x)
                    lats += abs(x[3]-lat_x)/(t-t_x)
                    alts += abs(x[4]-alt_x)/(t-t_x)
                #1.362885744927054e-05
            lng_x = x[2]
            lat_x = x[3]
            alt_x = x[4]
            t_x = t
    if i>0:
        a1.append(lngs/i)
        print(lngs/i)
        a2.append(lats/i)
        a3.append(alts/i)

#print(a1)
coor = np.vstack((a1,a2,a3)).T

fields = ['long','lat','alt']
filename = "gps_summery.csv"
with open(filename, 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
        
    csvwriter.writerow(fields) 
    csvwriter.writerows(coor)


# Create a dataframe
df = pd.read_csv("gps_summery.csv")
#df = pd.DataFrame(dt, fields)
print(df.to_numpy())
X = df.to_numpy()
kmeans = KMeans(n_clusters=3)                   # Number of clusters == 3
kmeans = kmeans.fit(X)                          # Fitting the input data
labels = kmeans.predict(X)                      # Getting the cluster labels
centroids = kmeans.cluster_centers_             # Centroid values
# print("Centroids are:", centroids)              # From sci-kit learn


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

x = np.array(labels==0)
y = np.array(labels==1)
z = np.array(labels==2)


ax.scatter(centroids[:,0],centroids[:,1],centroids[:,2],c="black",s=80,label="Centers",alpha=1)
ax.scatter(X[x,0],X[x,1],X[x,2],c="blue",s=40,label="C1")
ax.scatter(X[y,0],X[y,1],X[y,2],c="yellow",s=40,label="C2")
ax.scatter(X[z,0],X[z,1],X[z,2],c="red",s=40,label="C3")

ax.legend()
plt.show()
