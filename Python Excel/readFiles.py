import pandas as pd
from openpyxl.workbook import Workbook

df_excel = pd.read_excel("files/regions.xlsx")
df_csv = pd.read_csv("files/Names.csv", header=None)
df_txt = pd.read_csv("files/data.txt", delimiter='\t')

df_csv.columns = ['First Name', 'Last Name', 'Address', 'City', 'State', 'Pincode', 'Salary']

print(df_excel)
print(df_csv)
print(df_txt)