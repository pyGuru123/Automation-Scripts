import pandas as pd 
from openpyxl.workbook import Workbook 

df = pd.read_csv("files/Names.csv")
df.columns = ["First", "Last", "Address", "City", "State", "Code", "Salary"]

print(df.columns)
print(df)

# selecting columns
# print(df[["First", "Last", "State"]])
# print(df["Address"][0:3])


# selecting rows
print(df.iloc[1])

# selecting row & cols
print(df.iloc[1, 2])

# saving column data
wanted_cols = df[["First", "Last", "salary"]]
wanted_cols.to_excel("files/wanted_cols.xlsx")