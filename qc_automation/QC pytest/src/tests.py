import os
import sys
import logging
import pandas as pd

from src.autologger import Logger
from src.highlighter import highlight_logs

def test_CheckSampleLength(df, length, logger):
    # Check Number of rows in excel > mentioned in requirements
    assert len(df) >= length

def test_NoDuplicateRows(df, logger):
    # Tests if there'a duplicate values in the df based on name, phone, email_id
    duplicated = df[df.duplicated(subset=['First Name','Phone No', 'Work Email'], keep=False)]
    indices = duplicated.index.to_list()
    if indices:
        passed = False
        for i, index in enumerate(indices):
            logger.log(logging.DEBUG, f"{index+2}, duplicate values found for {duplicated.iloc[i]['First Name']}")

def test_RequiredColumnsNotEmpty(df, required_columns, logger):
    # Required Columns not empty
    for column in required_columns:
        nan = list(df.loc[pd.isna(df[column]), :].index)
        if nan:
            for index in nan:
                logger.log(logging.DEBUG, f"{index+2}, {column} value missing")

def test_MatchIndustries(df, industries, logger):
    # Tests if the industry column is in required industries
    for index, row in df.iterrows():
        industry = row['Industry'].lower()
        if industry not in industries:
            logger.log(logging.DEBUG, f"{index+2}, {industry} is not in required industries")

def test_LocationMatching(df, cities, states, countries, logger):
    # Matching locations based on keywords
    for index, row in df.iterrows():
        city = str(row['City']).lower()
        state = str(row['State']).lower()
        country = str(row['Country']).lower()

        if cities and city not in cities:
            logger.log(logging.DEBUG, f"{index+2}, city {city} not in required cities")

        if states and state not in states:
            logger.log(logging.DEBUG, f"{index+2}, state {state} not in required states")

        if countries and country not in countries:
            logger.log(logging.DEBUG, f"{index+2}, country {country} not in required countries")

def test_MatchDesignations(df, designations, logger):
    # Tests if the industry column is in allowed designations
    for index, row in df.iterrows():
        designation = str(row['Designation']).lower()
        if 'and' in designation:
            desgs = designation.split('and')
        elif '&' in designation:
            desgs = designation.split('&')
        else:
            desgs = [designation]
        
        count = 0
        for desg in desgs:
            if desg.strip() in designations:
                count += 1

        if count == 0:
            logger.log(logging.DEBUG, f"{index+2}, {designation} is not in allowed designations")

def test_NumberOfEmployessInRange(df, min_emp, max_emp, logger):
    # Tests if the number of employess are in the given range
    notInRange = df[(df['# Employees'] <= min_emp ) | (df['# Employees'] >= max_emp)]['# Employees']
    indices = notInRange.index.to_list()
    if indices:
        passed = False
        for i, index in enumerate(indices):
            logger.log(logging.DEBUG, f"{index+2}, Number of employess not in Range({min_emp},{max_emp})")

def test_MaxColumnsFilled(df, logger):
    # Maximum columns are filled with 10% max error
    total_cells = len(df) * len(df.columns)
    empty_columns = df.isna().sum().sum()
    perc = (empty_columns / total_cells) * 100
    if perc > 10:
        passed = False
        logger.log(logging.DEBUG, f"{-1}, {empty_columns} cells are not filled. ER = {perc:.1f}")

def test_ComapanyEmailMatching(df, logger):
    # tests if work email domain matching company website
    for index, row in df.iterrows():
        email = str(row['Work Email']).lower()
        company = str(row['Company']).lower()
        website = str(row['Website']).lower()

        company = ''.join(company.split())
        domain = email.split('@')[1].split('.')[0]
        if not (domain in company or domain in website):
            logger.log(logging.DEBUG, f"{index+2}, work email domain not matching company/website")

def test_AdditionalColumns(df, additional, logger):
    # check if additional columns exist in file
    columns = list(map(lambda x : x.lower(), list(df.columns)))
    for column in additional:
        if column not in columns:
            passed = False
            logger.log(logging.DEBUG, f"-1, additional column {column} not in file")

def test_additonalColumnsInReq(df, additional_req, logger):
    # check if additional columns are not empty
    test_frame = df.copy()
    test_frame.columns = map(str.lower, test_frame.columns)
    for column in additional_req:
        expected_values = additional_req[column]
        column_values = test_frame[column].to_list()
        for index, value in enumerate(column_values):
            if str(value).lower() not in expected_values:
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, {column} : {value} not in required values")

def test_validPhoneNumbers(df, logger):
    # Check which phone numbers are not valid
    phone_numbers = df['Phone Validation'].to_list()
    for index, phone in enumerate(phone_numbers):
        if phone.lower() != 'valid':
            passed = False
            logger.log(logging.DEBUG, f"{index+2}, phone number is invalid")

def test_socialProfileURLs(df, logger):
    # Check if the social profile urls are in correct column
    for index, row in df.iterrows():
        personal_linkedin = row['Person Linkedin Url']
        company_linkedin = row['Company Linkedin Url']
        facebook = row['Facebook Url']
        twitter = row['Twitter Url']

        if str(personal_linkedin) != 'nan' and 'linkedin' not in personal_linkedin:
            logger.log(logging.DEBUG, f"{index+2}, invalid personal linkedin url")

        if str(company_linkedin) != 'nan' and 'linkedin' not in company_linkedin:
            logger.log(logging.DEBUG, f"{index+2}, invalid company linkedin url")

        if str(facebook) != 'nan' and 'facebook' not in facebook:
            logger.log(logging.DEBUG, f"{index+2}, invalid facebook url")

        if str(twitter) != 'nan' and 'twitter' not in twitter:
            logger.log(logging.DEBUG, f"{index+2}, invalid twitter url")


############################# MAIN FUNCTION ###############################

def main(temp_file, log_file, requirements):
    logger = Logger(log_file)
    df = pd.read_excel(temp_file, sheet_name=1)

    required_columns = requirements["required_columns"]
    industries = requirements["industries"]
    cities = requirements["city"]
    states = requirements["state"]
    countries = requirements["country"]
    designations = requirements["desg_bucket"]
    length = requirements["sample_length"]
    min_emp = requirements["min_emp"]
    max_emp = requirements["max_emp"]
    additional = requirements["additional_columns"]
    additional_req = requirements["additional_req"]


    # FUNCTION CALLS ########################################
    test_CheckSampleLength(df, length, logger)
    test_NoDuplicateRows(df, logger)
    test_RequiredColumnsNotEmpty(df, required_columns, logger)
    test_MatchIndustries(df, industries, logger)
    test_LocationMatching(df, cities, states, countries, logger)
    test_MatchDesignations(df, designations, logger)
    test_NumberOfEmployessInRange(df, min_emp, max_emp, logger)
    test_MaxColumnsFilled(df, logger)
    test_ComapanyEmailMatching(df, logger)
    test_AdditionalColumns(df, additional, logger)
    test_additonalColumnsInReq(df, additional_req, logger)
    test_validPhoneNumbers(df, logger)
    test_socialProfileURLs(df, logger)

    # HIGHLIGHTER #############################################
    # highlight_logs(temp_file, log_file)

    return True