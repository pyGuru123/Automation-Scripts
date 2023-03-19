import pandas as pd
from openpyxl.workbook import Workbook 

df = pd.read_csv("files/Names.csv", header=None)
df.columns = ["First", "Last", "Address", "City", "State", "Code", "Salary"]

columns_to_drop = ['Code', 'First', 'Address']
df.drop(columns=columns_to_drop, inplace=True)

df['Tax %'] = df['Salary'].apply(lambda x : .15 if 10000< x <40000 else .20 if 40000 < 80000 else .25)
df['Tax owed'] = df['Salary'] * df['Tax %']

df['Status'] = False
df.loc[df['Salary'] < 40000, 'Status'] = True
print(df.sort_values('Salary', ascending=False))

print(df.groupby(['Status']).mean())