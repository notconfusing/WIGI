#! /usr/bin/env python

from __future__ import print_function
import pandas as pd
import numpy as np


def preview(data):
    print(data.head(2))
    print(data.describe())


def pre_process(data, missing_value=0, drop_nan=True):
    if drop_nan:
        data = data.drop('nan', 1)
    return data.fillna(value=missing_value)


def ids_set(data):
    unique_qids = set()
    data_qids = data.iloc[:, 0] # get all fields
    for qid_row in data_qids:
        _qids = qid_row.strip('|').split('|')
        for qid in _qids:
            unique_qids.add(qid)

    print("Found {} unique qids.".format(len(data)))
    return unique_qids


def flatten(data, unique_qids=None):
    data = pre_process(data)
    if unique_qids is None:
        unique_qids = ids_set(data)

    columns = data.columns[1:]
    dataframe = pd.DataFrame(0, index=unique_qids, columns=columns)

    # number of columns to skip when adding data.
    # current number corresponds to serial number and qid.
    skip = 2
    for row in data.itertuples():
        # row[0] is index, row[1] is data tuple
        _fields = row[1].strip('|').split('|')
        for field in _fields:
            for column in enumerate(columns):
                dataframe.loc[field, column[1]] += row[column[0] + skip]

    # XXX: this is a hack for the "occupation-index.csv" files whose's first
    # columns is unnamed by default.
    new_columns = dataframe.columns.values
    new_columns[0] = 'qid'
    dataframe.columns = new_columns

    return dataframe

if __name__ == '__main__':
    from sys import argv, exit
    from os import path

    if len(argv) < 2:
        print("Usage: flatten.py <input file>\n"
              "Returns a file with name flat_<input file> in same directory.")
        exit(0)
    datafile = argv[1]

    data = pd.read_csv(path.abspath(datafile))
    preview(data)

    flattened_df = flatten(data)

    preview(flattened_df)
    flattened_df.to_csv('flat_{}'.format(datafile))
