import numpy as np
import pandas as pd

from scipy.spatial import distance_matrix

c1 = ['1', '2', '3']

c2 = ['4', '5', '6']

cc = np.vstack((c1,c2))
fields = ['c1','c2']
ccc = pd.DataFrame(cc, np.array(fields)).T

print(ccc)
