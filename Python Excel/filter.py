import pandas as pd 
from openpyxl.workbook import Workbook 

df = pd.read_csv("files/Names.csv", header=None)
df.columns = ["First", "Last", "Address", "City", "State", "Code", "Salary"]

new_df = df.loc[df['City'] == 'Riverside']
indices = new_df.index.to_list()
print(new_df)
print(indices)

print(df.loc[(df['City'] == 'Riverside') & (df['First'] == 'John')])

# adding new columns
df['Tax %'] = df['Salary'].apply(lambda x : .15 if 10000< x <40000 else .20 if 40000 < 80000 else .25)
df['Tax owed'] = df['Salary'] * df['Tax %']
print(df)