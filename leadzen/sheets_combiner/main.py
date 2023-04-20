import tempfile
import pandas as pd
from loguru import logger
from typing import BinaryIO

def main(excel_file: BinaryIO, filename: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        lines = excel_file.readlines()
        temp_file.writelines(lines)
        temp_file.seek(0)

        # df = pd.read_excel(temp_file)
        temp_df = pd.ExcelFile(temp_file)
        # print(temp_df.sheet_names)
        for sheet in temp_df.sheet_names:
        	df = pd.read_excel(temp_file, sheet_name=sheet)
        	print(sheet, df.columns)