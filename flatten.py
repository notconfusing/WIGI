import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fow = pd.read_csv('field_of_work-index.csv')

# preview data
print fow.head(2)
print fow.describe()

# remove missing values
nfow = fow.fillna(value=0)

# get all fields
fow_flat_names = set()
fow_names = nfow.iloc[:, 0]
for name in fow_names:
    _name = name.strip('|').split('|')
    for item in _name:
        fow_flat_names.add(item)

print len(fow_flat_names)

# new dataframe
fow_new = pd.DataFrame(0, index=fow_flat_names,
                       columns=['transgender male', 'female', 'male'])

for row in nfow.iterrows():
    # row[0] is index, row[1] is data tuple
    _data = row[1]
    _fields = _data[0].strip('|').split('|')
    for field in _fields:
        fow_new.loc[field, 'male'] += _data['male']
        fow_new.loc[field, 'female'] += _data['female']
        fow_new.loc[field, 'transgender male'] += _data['transgender male']

# preview
print fow_new.head(2)
print fow_new.describe()

# write to csv
fow_new.to_csv('flatten_field_of_work-index.csv')
