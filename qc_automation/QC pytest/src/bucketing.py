import math
import pandas as pd

bucketing_file = "src\BUCKETING.xlsx"
df = pd.read_excel(bucketing_file, sheet_name=0)
BUCKET = {}

def removeNan(column):
    # Removes Nan values from a list
    return list(filter(lambda ele: str(ele) != 'nan', column))

def df_column(column):
    # Returns the df column removing Nan
    return removeNan(column.to_list())

# Adding Columns to BUCKET dictionary
columns = df.columns
for column in columns:
    BUCKET[column.lower()] = df_column(df[column])

# Loading Abbreviations
abbreviations = pd.read_excel(bucketing_file, sheet_name=1)
abbs = abbreviations.iloc[:, 0].to_list()
abbs = list(map(lambda x : x.lower(), abbs))
newBucket = {senior : BUCKET[senior] for senior in BUCKET}
for senior in BUCKET:
    for position in BUCKET[senior]:
        if position.lower() in abbs:
            index = abbs.index(position.lower())
            row = df_column(abbreviations.iloc[index])
            newBucket[senior] = list(set(newBucket[senior] + row))
            
BUCKET = newBucket

########### BUCKET Columns ###########
# Owner
# CxO
# Director
# Partner
# Senior
# VP
# Manager
# Entry
# Training
# Unpaid