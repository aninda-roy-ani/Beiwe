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

# Create a dataframe
df = pd.read_csv("gps_night.csv")
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

# %%

