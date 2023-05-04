import asyncio
import tempfile
import numpy as np
import pandas as pd
from loguru import logger
from typing import BinaryIO

from app.sheets_combiner.config import (
    get_all_apollo_columns,
    get_required_apollo_columns,
    apollo_renamed_columns,
    rocket_renamed_columns,
    sn_renamed_columns,
    sheet_names
)

from app.sheets_combiner.operia_details_fetcher import (
    fetch_company_details
)

from app.sheets_combiner.company import (
    get_company_names,
    company_website,
    fill_company_website,
    get_companies_with_no_company_linkedin,
    fill_companies_with_company_linkedin
)

from app.sheets_combiner.linkedin_url import (
    linkedin_url_fast
)

def split_string_to_three_substrings(value, by):
    if str("value") != "nan":
        loc = str(value).split(by)[:3]
        loc = list(map(lambda x: x.strip(), loc))
        loc = [" "]*(3-len(loc)) + loc
    else:
        loc = [" ", " ", " "]

    return loc

def split_column_to_three_columns(column, by):
    splitted_columns = []
    for index, value in column.iteritems():
        loc = split_string_to_three_substrings(value, by)
        splitted_columns.append(loc)

    return splitted_columns

def get_not_required_columns(column_list_1, column_list_2):
    return list(set(column_list_1) - set(column_list_2))

def fix_apollo(df):
    df = df.dropna(how="all")

    rename_column_dict = apollo_renamed_columns()
    df = df.rename(columns=rename_column_dict)

    not_required_columns = get_not_required_columns(df.columns, get_required_apollo_columns())
    df = df.drop(columns=not_required_columns)

    return df

def fix_rocket(df):
    df = df.dropna(how="all")

    df[["First Name", "Last Name"]] = df["name"].str.split(" ", n=1, expand=True)
    df[["City", "State", "Country"]] = split_column_to_three_columns(df['location'], by=",")

    rename_column_dict = rocket_renamed_columns()
    df = df.rename(columns=rename_column_dict)

    not_required_columns = get_not_required_columns(df.columns, get_required_apollo_columns())
    df = df.drop(columns=not_required_columns)
    
    return df

def fix_sn(df):
    df = df.dropna(how="all")

    df[["City", "State", "Country"]] = split_column_to_three_columns(df['location'], by=",")
    
    rename_column_dict = sn_renamed_columns()
    df = df.rename(columns=rename_column_dict)

    not_required_columns = get_not_required_columns(df.columns, get_required_apollo_columns())
    df = df.drop(columns=not_required_columns)
    
    return df

def fill_company_details(df, company_details):
    for company in company_details:
        location = company["location"]
        address, city, state, country = "", "", "", ""
        if len(location) > 0: 
            address = location[0].get("address", "")
            address_2 = location[0].get("address_2", "")
            city, state, country = split_string_to_three_substrings(address_2, ",")

        columns = ["Company Linkedin Url", "Company", "Website", "Industry", "# Employees", "Company Address",
                 "Company City", "Company State", "Company Country"
                 ]
        column_values = [
            company["Company Linkedin Url"],
            company["Company"],
            company["Website"],
            company["Industry"],
            company["# Employees"],
            address,
            city,
            state,
            country
        ]

        df.loc[df['Company Linkedin Url'] == company["id"], columns] = column_values

    return df


def main(excel_file: BinaryIO, filename: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        lines = excel_file.readlines()
        temp_file.writelines(lines)
        temp_file.seek(0)

        sheets = sheet_names(temp_file)

        dataframes = []
        for sheet in sheets:
            df = pd.read_excel(temp_file, sheet_name=sheet)
            df.reset_index(inplace=True, drop=True)

            if "apollo" in sheet.lower():
                dataframes.append(fix_apollo(df))
            elif "rocket" in sheet.lower():
                dataframes.append(fix_rocket(df))
            elif "navigator" in sheet.lower():
                dataframes.append(fix_sn(df))

        # merge the 3 sheets in 1 dataframe
        df = pd.concat(dataframes, ignore_index=True)
        df.replace(['not available', 'N/A'], np.nan, inplace=True)

        # fetch company linkedin urls
        try:
            companies = get_companies_with_no_company_linkedin(df)
            company_linkedin_ids = asyncio.run(linkedin_url_fast(companies))
            df = fill_companies_with_company_linkedin(df, company_linkedin_ids)
        except Exception as e:
            logger.error(e)

        # # fetch company details from operia and fill in dataframe
        # try:
        #     company_details = asyncio.run(fetch_company_details(df))
        #     df = fill_company_details(df, company_details)
        # except Exception as e:
        #     logger.error(e)

        # # get company names with no websites
        # try:
        #     company_names = get_company_names(df)
        #     company_websites = asyncio.run(company_website(company_names))
        #     df = fill_company_website(df, company_websites)
        # except Exception as e:
        #     logger.error(e)

        # export dataframe to excel
        df.to_excel(filename, index=None)