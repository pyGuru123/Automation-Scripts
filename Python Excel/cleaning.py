import numpy as np
import pandas as pd 
from openpyxl.workbook import Workbook

df = pd.read_csv("files/Names.csv", header=None)
df.columns = ["First", "Last", "Address", "City", "State", "Code", "Salary"]

df.drop(columns='Address', inplace=True)
df = df.set_index('Code')
print(df)
print(df.loc[8075, 'State'])
print(df.loc[8074])
print(df.loc[8074:, 'First'])
print(df.First)
df.First = df.First.str.split(expand=True)[0]

df = df.replace(np.nan, 'N/A', regex=True)
print(df)