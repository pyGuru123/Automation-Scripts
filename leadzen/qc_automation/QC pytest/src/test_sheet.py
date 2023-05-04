import os
import sys
import pytest
import logging
import pandas as pd

from src.autologger import Logger

if len(sys.argv) == 5:
    FILE = sys.argv[2]
    FILENAME = sys.argv[3]
    REQUIREMENTS = sys.argv[4]

    log_file = os.path.splitext(FILENAME)[0] + ".txt"


    ################ LOGGING CONFIG ###################

    logger = Logger(log_file)

    ################ TESTING CHECKLIST #################

    @pytest.fixture()
    def df():
        # Making df available to all tests
        df = pd.read_excel(FILE, sheet_name=1)
        return df

    @pytest.mark.parametrize("length", [(SAMPLE_LENGTH)])
    def test_CheckSampleLength(df, length):
        # Check Number of rows in excel > mentioned in requirements
        assert len(df) >= length

    def test_NoDuplicateRows(df):
        # Tests if there'a duplicate values in the df based on name, phone, email_id
        passed = True
        duplicated = df[df.duplicated(subset=['First Name','Phone No', 'Work Email'], keep=False)]
        indices = duplicated.index.to_list()
        if indices:
            passed = False
            for i, index in enumerate(indices):
                logger.log(logging.DEBUG, f"{index+2}, duplicate values found for {duplicated.iloc[i]['First Name']}")

        assert passed

    @pytest.mark.parametrize("required_columns", [(REQUIRED_COLUMNS)])
    def test_RequiredColumnsNotEmpty(df, required_columns):
        # Required Columns not empty
        passed = True
        for column in required_columns:
            nan = list(df.loc[pd.isna(df[column]), :].index)
            if nan:
                passed = False
                for index in nan:
                    logger.log(logging.DEBUG, f"{index+2}, {column} value missing")

        assert passed

    @pytest.mark.parametrize("industries", [(INDUSTRIES)])
    def test_MatchIndustries(df, industries):
        # Tests if the industry column is in required industries
        passed = True
        for index, row in df.iterrows():
            industry = row['Industry'].lower()
            if industry not in industries:
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, {industry} is not in required industries")

        assert passed

    @pytest.mark.parametrize("cities, states, countries", [(CITY, STATE, COUNTRY)])
    def test_LocationMatching(df, cities, states, countries):
        # Matching locations based on keywords
        passed = True
        for index, row in df.iterrows():
            city = str(row['City']).lower()
            state = str(row['State']).lower()
            country = str(row['Country']).lower()

            if cities and city not in cities:
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, city {city} not in required cities")

            if states and state not in states:
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, state {state} not in required states")

            if countries and country not in countries:
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, country {country} not in required countries")

        assert passed

    @pytest.mark.parametrize("designations", [(DESG_BUCKET)])
    def test_MatchDesignations(df, designations):
        # Tests if the industry column is in allowed designations
        passed = True
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
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, {designation} is not in allowed designations")

        assert passed

    @pytest.mark.parametrize("min_emp, max_emp", [(MIN_EMP, MAX_EMP)])
    def test_NumberOfEmployessInRange(df, min_emp, max_emp):
        # Tests if the number of employess are in the given range
        passed = True
        notInRange = df[(df['# Employees'] <= min_emp ) | (df['# Employees'] >= max_emp)]['# Employees']
        indices = notInRange.index.to_list()
        if indices:
            passed = False
            for i, index in enumerate(indices):
                logger.log(logging.DEBUG, f"{index+2}, Number of employess not in Range({min_emp},{max_emp})")

        assert passed

    def test_MaxColumnsFilled(df):
        # Maximum columns are filled with 10% max error
        passed = True
        total_cells = len(df) * len(df.columns)
        empty_columns = df.isna().sum().sum()
        perc = (empty_columns / total_cells) * 100
        if perc > 10:
            passed = False
            logger.log(logging.DEBUG, f"{-1}, {empty_columns} cells are not filled. ER = {perc:.1f}")

        assert passed

    def test_ComapanyEmailMatching(df):
        # tests if work email domain matching company website
        passed = True
        for index, row in df.iterrows():
            email = str(row['Work Email']).lower()
            company = str(row['Company']).lower()
            website = str(row['Website']).lower()

            company = ''.join(company.split())
            domain = email.split('@')[1].split('.')[0]
            if not (domain in company or domain in website):
                logger.log(logging.DEBUG, f"{index+2}, work email domain not matching company/website")

        assert passed

    @pytest.mark.parametrize("additional", [(ADDITIONAL_COLUMNS)])
    def test_AdditionalColumns(df, additional):
        # check if additional columns exist in file
        passed = True
        columns = list(map(lambda x : x.lower(), list(df.columns)))
        for column in additional:
            if column not in columns:
                passed = False
                logger.log(logging.DEBUG, f"-1, additional column {column} not in file")

        assert passed

    @pytest.mark.parametrize("additional_req", [(ADDITIONAL_REQ)])
    def test_additonalColumnsInReq(df, additional_req):
        # check if additional columns are not empty
        passed = True
        test_frame = df
        test_frame.columns = map(str.lower, test_frame.columns)
        for column in additional_req:
            expected_values = additional_req[column]
            column_values = test_frame[column].to_list()
            for index, value in enumerate(column_values):
                if str(value).lower() not in expected_values:
                    passed = False
                    logger.log(logging.DEBUG, f"{index+2}, {column} : {value} not in required values")

        assert passed


    def test_validPhoneNumbers(df):
        # Check which phone numbers are not valid
        passed = True
        phone_numbers= df['Phone Validation'].to_list()
        for index, phone in enumerate(phone_numbers):
            if phone.lower() != 'valid':
                passed = False
                logger.log(logging.DEBUG, f"{index+2}, phone number is invalid")

        return passed

    def test_socialProfileURLs(df):
        # Check if the social profile urls are in correct column
        passed = True
        for index, row in df.iterrows():
            personal_linkedin = row['Person Linkedin Url']
            company_linkedin = row['Company Linkedin Url']
            facebook = row['Facebook Url']
            twitter = row['Twitter Url']

            if str(personal_linkedin) != 'nan' and 'linkedin' not in personal_linkedin:
                logger.log(logging.DEBUG, f"{index+2}, invalid personal linkedin url")
                passed = False

            if str(company_linkedin) != 'nan' and 'linkedin' not in company_linkedin:
                logger.log(logging.DEBUG, f"{index+2}, invalid company linkedin url")
                passed = False

            if str(facebook) != 'nan' and 'facebook' not in facebook:
                logger.log(logging.DEBUG, f"{index+2}, invalid facebook url")
                passed = False

            if str(twitter) != 'nan' and 'twitter' not in twitter:
                logger.log(logging.DEBUG, f"{index+2}, invalid twitter url")
                passed = False

        assert passed