import os
import json
import requests
import pandas as pd

bucketing_file = "BUCKETING.xlsx"

def getBucket() -> dict:
    df = pd.read_excel(bucketing_file, sheet_name=0)

    bucket = {}
    columns = df.columns
    for column in columns:
        column_values = df[column].dropna().to_list()
        bucket[column.lower()] = column_values

    abbreviations = pd.read_excel(bucketing_file, sheet_name=1)
    first_column = abbreviations.iloc[:, 0].to_list()
    first_column = list(map(lambda x: x.lower(), first_column))

    newBucket = {}
    for senior in bucket:
        newBucket[senior] = bucket[senior]

    for senior in bucket:
        for position in bucket[senior]:
            if position.lower() in first_column:
                index = first_column.index(position.lower())
                row = abbreviations.iloc[index].dropna().to_list()
                newBucket[senior] = list(set(newBucket[senior] + row))

    # return newBucket
    with open("bucket.json", 'w') as json_file:
        json.dump(newBucket, json_file)

getBucket()
