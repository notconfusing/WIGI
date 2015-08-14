import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

occ = pd.read_csv('occupation-index.csv')

# preview data
print occ.head(2)
print occ.describe()

# remove missing values
nocc = occ.fillna(value=0)

# get all fields
occ_flat_names = set()
occ_names = nocc.iloc[:, 0]
for name in occ_names:
    _name = name.strip('|').split('|')
    for item in _name:
        occ_flat_names.add(item)

print len(occ_flat_names)

# new dataframe
columns = occ.columns[2:]
occ_new = pd.DataFrame(0, index=occ_flat_names,
                       columns=columns)

for data in nocc.itertuples():
    # row[0] is index, row[1] is data tuple
    _fields = data[1].strip('|').split('|')
    for field in _fields:
        for column in enumerate(columns):
            occ_new.loc[field, column[1]] += data[column[0] + 3]

# preview
print occ_new.head(2)
print occ_new.describe()

# write to csv
occ_new.to_csv('flatten_occupation-index.csv')
