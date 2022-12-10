import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def dataFrame( column_to_drop, filename ):

    dataFrame = pd.read_csv(filename)
    dataFrame.drop(column_to_drop, axis=1, inplace=True)

    return dataFrame


def number_of_clusters( dataFrame ):

    scores = []
    limit = int((dataFrame.shape[0]//2)**0.5)

    for k in range(2, limit+1):
        model = KMeans(n_clusters=k)
        model.fit(dataFrame)
        pred = model.predict(dataFrame)
        score = silhouette_score(dataFrame, pred)
        scores.append(score)
        print(score)
    
    print()
    u = 2
    return scores.index(max(scores)) + u


file_name = "gps_standard_deviation_eachParticipant.csv"

print(number_of_clusters(dataFrame('PARTICIPANTS', file_name)))
