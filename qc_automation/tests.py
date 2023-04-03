import os
import sys
import logging
import openpyxl
import tempfile
import pandas as pd
from loguru import logger
from typing import BinaryIO, Callable

from app.qc_automation.autologger import Logger
from app.qc_automation.config import (
    get_constraints,
    get_exclusion,
    remove_https,
)
from app.qc_automation.highlighter import highlight_logs


def exception_handler(func: Callable) -> Callable:
    def wrapper(*args):
        try:
            func(*args)
        except Exception as e:
            logger.error(f"An Exception occured in {func.__name__}: {e}")
        return None

    return wrapper


@exception_handler
def test_check_sample_length(
    df: pd.DataFrame, length: int, file_logger: logging.Logger
) -> None:
    if not len(df) >= length:
        file_logger.log(
            logging.DEBUG,
            f"{len(df)+2}@1: length of excel file less than requirement",
        )


@exception_handler
def test_no_duplicate_rows(df: pd.DataFrame, file_logger: logging.Logger) -> None:
    duplicated = df[
        df.duplicated(subset=["first name", "primary phone", "work email"], keep=False)
    ]
    indices = duplicated.index.to_list()
    if indices:
        for i, index in enumerate(indices):
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@1: duplicate values found for {duplicated.iloc[i]['First Name']}",
            )


@exception_handler
def test_required_columns_not_empty(
    df: pd.DataFrame, required_columns: list, file_logger: logging.Logger
) -> None:
    for column in required_columns:
        column_index = list(df.columns).index(column) + 1
        nan = list(df.loc[pd.isna(df[column]), :].index)
        if nan:
            for index in nan:
                file_logger.log(
                    logging.DEBUG,
                    f"{index+2}@{column_index}: {column} value missing",
                )


@exception_handler
def test_match_industries(
    df: pd.DataFrame, industries: list, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("industry") + 1
    for index, row in df.iterrows():
        industry = row["industry"].lower()
        if industry not in industries:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: {industry} is not in required industries",
            )


@exception_handler
def test_location_matching(
    df: pd.DataFrame,
    cities: list,
    states: list,
    countries: list,
    file_logger: logging.Logger,
) -> None:
    city_index = list(df.columns).index("city") + 1
    state_index = list(df.columns).index("state") + 1
    country_index = list(df.columns).index("country") + 1

    for index, row in df.iterrows():
        city = str(row["city"]).lower()
        state = str(row["state"]).lower()
        country = str(row["country"]).lower()

        if cities and city not in cities:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{city_index}: city {city} not in required cities",
            )

        if states and state not in states:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{state_index}: state {state} not in required states",
            )

        if countries and country not in countries:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{country_index}: country {country} not in required countries",
            )


@exception_handler
def test_match_designations(
    df: pd.DataFrame, designations: list, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("designation") + 1

    for index, row in df.iterrows():
        designation = str(row["designation"]).lower()
        if "and" in designation:
            desgs = designation.split("and")
        elif "&" in designation:
            desgs = designation.split("&")
        else:
            desgs = [designation]

        count = 0
        for desg in desgs:
            if desg.strip() in designations:
                count += 1

        if count == 0:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: {designation} is not in allowed designations",
            )


@exception_handler
def test_number_of_employess_in_range(
    df: pd.DataFrame, min_emp: int, max_emp: int, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("# employees") + 1

    notInRange = df[(df["# employees"] <= min_emp) | (df["# employees"] >= max_emp)][
        "# employees"
    ]
    indices = notInRange.index.to_list()
    if indices:
        for i, index in enumerate(indices):
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: Number of employess not in Range({min_emp},{max_emp})",
            )


@exception_handler
def test_max_columns_filled(df: pd.DataFrame, file_logger: logging.Logger) -> None:
    total_cells = len(df) * len(df.columns)
    empty_columns = df.isna().sum().sum()
    perc = (empty_columns / total_cells) * 100
    if perc > 10:
        file_logger.log(
            logging.DEBUG,
            f"{len(df)+2}@1: {empty_columns} cells are not filled. ER = {perc:.1f}",
        )


@exception_handler
def test_comapany_email_matching(df: pd.DataFrame, file_logger: logging.Logger) -> None:
    column_index = list(df.columns).index("work email") + 1

    for index, row in df.iterrows():
        email = str(row["work email"]).lower()
        company = str(row["company"]).lower()
        website = str(row["website"]).lower()

        company = "".join(company.split())
        domain = email.split("@")[1].split(".")[0]
        if not (domain in company or domain in website):
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: work email domain not matching company/website",
            )


@exception_handler
def test_additional_columns(
    df: pd.DataFrame, additional: list, file_logger: logging.Logger
) -> None:
    columns = list(df.columns)
    for column in additional:
        if column not in columns:
            file_logger.log(
                logging.DEBUG,
                f"{len(df)+2}@1: additional column {column} not in file",
            )


@exception_handler
def test_valid_phone_and_emails(df: pd.DataFrame, file_logger: logging.Logger) -> None:
    if "phone verified" in list(df.columns):
        column_index = list(df.columns).index("phone verified") + 1
        phone_numbers = df["phone verified"].to_list()
        for index, phone in enumerate(phone_numbers):
            if phone.lower() != "valid":
                file_logger.log(
                    logging.DEBUG,
                    f"{index+2}@{column_index}: phone number is invalid",
                )

    if "email verified" in list(df.columns):
        column_index = list(df.columns).index("email verified") + 1
        phone_numbers = df["email verified"].to_list()
        for index, phone in enumerate(phone_numbers):
            if phone.lower() != "valid":
                file_logger.log(
                    logging.DEBUG,
                    f"{index+2}@{column_index}: email is invalid",
                )


@exception_handler
def test_social_profile_urls(df: pd.DataFrame, file_logger: logging.Logger) -> None:
    plink = list(df.columns).index("person linkedin url") + 1
    clink = list(df.columns).index("company linkedin url") + 1
    falink = list(df.columns).index("facebook url") + 1
    twlink = list(df.columns).index("twitter url") + 1

    for index, row in df.iterrows():
        personal_linkedin = row["person linkedin url"]
        company_linkedin = row["company linkedin url"]
        facebook = row["facebook url"]
        twitter = row["twitter url"]

        if str(personal_linkedin) != "nan" and "linkedin" not in personal_linkedin:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{plink}: invalid personal linkedin url",
            )

        if str(company_linkedin) != "nan" and "linkedin" not in company_linkedin:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{clink}: invalid company linkedin url",
            )

        if str(facebook) != "nan" and "facebook" not in facebook:
            file_logger.log(logging.DEBUG, f"{index+2}@{falink}: invalid facebook url")

        if str(twitter) != "nan" and "twitter" not in twitter:
            file_logger.log(logging.DEBUG, f"{index+2}@{twlink}: invalid twitter url")


@exception_handler
def test_excluded_phone_numbers(
    df: pd.DataFrame, ex_list: list, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("primary phone") + 1
    for index, phone in enumerate(df["primary phone"].to_list()):
        if phone in ex_list:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: Phone number in exclusion list",
            )


@exception_handler
def test_excluded_emails(
    df: pd.DataFrame, ex_list: list, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("work email") + 1
    for index, phone in enumerate(df["work email"].to_list()):
        if phone in ex_list:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: Email in exclusion list",
            )

    column_index = list(df.columns).index("personal email") + 1
    for index, phone in enumerate(df["personal email"].to_list()):
        if phone in ex_list:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: Email in exclusion list",
            )


@exception_handler
def test_excluded_websites(
    df: pd.DataFrame, ex_list: list, file_logger: logging.Logger
) -> None:
    column_index = list(df.columns).index("website") + 1
    for index, website in enumerate(df["website"].to_list()):
        website = remove_https(website)
        if website in ex_list:
            file_logger.log(
                logging.DEBUG,
                f"{index+2}@{column_index}: Website in exclusion list",
            )


@exception_handler
def test_count_people_per_company(
    df: pd.DataFrame, limit: int, file_logger: logging.Logger
):
    if str(limit).isdigit():
        column_index = list(df.columns).index("company")
        counts = df["company"].value_counts()
        groups = dict(df.groupby("company").groups)
        for company in groups:
            count = groups[company]
            if len(count) > limit:
                for index in count[limit:]:
                    if column_index == 0:
                        column_index = 1
                    file_logger.log(
                        logging.DEBUG,
                        f"{index+2}@{column_index}: number of people per company > requirements",
                    )


############################# MAIN FUNCTION ###############################


def main(excel_file: BinaryIO, log_file: str, filename: str):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        lines = excel_file.readlines()
        temp_file.writelines(lines)
        temp_file.seek(0)

        requirements = get_constraints(temp_file)
        exclusion_dict = get_exclusion(temp_file)

        file_logger = Logger(log_file)
        df = pd.read_excel(temp_file, sheet_name=1)
        df.columns = [column.lower() for column in list(df.columns)]

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
        people_per_company = requirements["people_per_company"]

        # FUNCTION CALLS ########################################
        test_check_sample_length(df, length, file_logger)
        test_no_duplicate_rows(df, file_logger)
        test_required_columns_not_empty(df, required_columns, file_logger)
        test_match_industries(df, industries, file_logger)
        test_location_matching(df, cities, states, countries, file_logger)
        test_match_designations(df, designations, file_logger)
        test_number_of_employess_in_range(df, min_emp, max_emp, file_logger)
        test_max_columns_filled(df, file_logger)
        test_comapany_email_matching(df, file_logger)
        test_additional_columns(df, additional, file_logger)
        # test_additonalColumnsInReq(df, additional_req, file_logger)
        test_valid_phone_and_emails(df, file_logger)
        test_social_profile_urls(df, file_logger)
        test_excluded_phone_numbers(df, exclusion_dict["phone"], file_logger)
        test_excluded_emails(df, exclusion_dict["email"], file_logger)
        test_excluded_websites(df, exclusion_dict["website"], file_logger)
        test_count_people_per_company(df, people_per_company, file_logger)

        # HIGHLIGHTER #############################################
        highlight_logs(temp_file, filename, log_file)
