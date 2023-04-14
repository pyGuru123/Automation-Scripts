import pandas as pd
from loguru import logger
from typing import BinaryIO
from app.qc_automation.bucketing import load_bucket

row_num = 0


def splitByComma(string: str) -> list:
    if str(string) != "nan":
        return list(map(lambda x: x.strip().lower(), string.split(",")))
    return []


def fix_revenue(revenue: str) -> int:
    if revenue != "nan":
        return int(float(revenue))
    return 0


def get_industries(df: pd.DataFrame) -> list[str]:
    industries = []
    if "industry" in df.columns:
        industries = splitByComma(df.loc[row_num, "industry"])
    return industries


def get_person_location(df: pd.DataFrame) -> list[list[str]]:
    city = []
    state = []
    country = []

    if "city" in df.columns and str(df.loc[row_num, "city"]).lower() != "n/a":
        city = splitByComma(df.loc[row_num, "city"])
    if "state" in df.columns and str(df.loc[0, "state"]).lower() != "n/a":
        state = splitByComma(df.loc[row_num, "state"])
    if "country" in df.columns and str(df.loc[0, "country"]).lower() != "n/a":
        country = splitByComma(df.loc[row_num, "country"])

    return [city, state, country]


def get_company_location(df: pd.DataFrame) -> list[list[str]]:
    company_city = []
    company_state = []
    company_country = []

    if (
        "company city" in df.columns
        and str(df.loc[row_num, "company city"]).lower() != "n/a"
    ):
        company_city = splitByComma(df.loc[row_num, "company city"])
    if (
        "company state" in df.columns
        and str(df.loc[0, "company state"]).lower() != "n/a"
    ):
        company_state = splitByComma(df.loc[row_num, "company state"])
    if (
        "company country" in df.columns
        and str(df.loc[0, "company country"]).lower() != "n/a"
    ):
        company_country = splitByComma(df.loc[row_num, "company country"])

    return [company_city, company_state, company_country]


def get_sample_length(df: pd.DataFrame) -> int:
    return df.loc[row_num, "quantity"] or 1


def get_designation_bucket(df: pd.DataFrame) -> dict[str, list]:
    designation = []
    if str(df.loc[row_num, "designation"]).lower() != "n/a":
        BUCKET = load_bucket()
        designation = splitByComma(df.loc[row_num, "designation"])
        desg_bucekt = []
        for desg in designation:
            if desg in BUCKET:
                desg_bucekt += BUCKET[desg]
            else:
                desg_bucekt.append(desg)
        desg_bucekt = list(map(lambda x: x.lower(), desg_bucekt))

    return desg_bucekt


def get_number_of_employees(df: pd.DataFrame) -> list[int]:
    min_emp, max_emp = 0, 50000000
    if "# employees" in df.columns:
        num_emp = df.loc[row_num, "# employees"]
        if str(num_emp) != "n/a":
            min_emp, max_emp = map(int, num_emp.split("-"))

    return [min_emp, max_emp]


def get_additional_columns(df: pd.DataFrame) -> list[str]:
    additional_columns = []
    if "additional columns" in df.columns:
        additional_column_value = str(df.loc[row_num, "additional columns"]).lower()
        if additional_column_value != "n/a":
            additional_columns = splitByComma(df.loc[row_num, "additional columns"])
            additional_columns = list(map(lambda x: x.lower(), additional_columns))

    return additional_columns


def get_additional_requirements(df: pd.DataFrame) -> dict[str, list]:
    additional_req = {}
    if "additional columns" in df.columns:
        additional_columns = get_additional_columns(df)
        for column in additional_columns:
            if column in df.columns:
                additional_req[column] = splitByComma(df.loc[row_num, column])

    return additional_req


def get_people_per_company(df: pd.DataFrame) -> int:
    people_per_company = 0
    if "number of people/company" in df.columns:
        people_per_company = df.loc[row_num, "number of people/company"]

    return people_per_company


def get_phone_codes(df: pd.DataFrame) -> list[str]:
    if "phone codes" in df.columns:
        codes = splitByComma(df.loc[row_num, "phone codes"])
        phone_codes = ["+" + code for code in codes]
        return phone_codes
    return [
        "+91",
    ]


def get_currency(df: pd.DataFrame) -> list[str]:
    if "currency" in df.columns:
        currency = splitByComma(df.loc[row_num, "currency"])
        return currency
    return ["₹"]


def get_annual_revenue_range(df: pd.DataFrame) -> list[int]:
    min_revenue = -1
    max_revenue = -1
    if "min revenue" in df.columns:
        revenue = str(df.loc[row_num, "min revenue"])
        if str(revenue) != "nan":
            min_revenue = fix_revenue(revenue)
    if "max revenue" in df.columns:
        revenue = str(df.loc[row_num, "max revenue"])
        if str(revenue) != "nan":
            max_revenue = fix_revenue(revenue)

    return [min_revenue, max_revenue]


def get_constraints(temp_file: BinaryIO) -> dict:
    df = pd.read_excel(temp_file)
    df.columns = [column.lower() for column in list(df.columns)]

    required_columns = ["first name", "company", "primary phone", "work email"]
    industries = get_industries(df)
    city, state, country = get_person_location(df)
    company_city, company_state, company_country = get_company_location(df)
    sample_length = get_sample_length(df)
    desg_bucket = get_designation_bucket(df)
    min_emp, max_emp = get_number_of_employees(df)
    additional_columns = get_additional_columns(df)
    additional_req = get_additional_requirements(df)
    people_per_company = get_people_per_company(df)
    phone_codes = get_phone_codes(df)
    currency = get_currency(df)
    revenue_range = get_annual_revenue_range(df)

    return {
        "required_columns": required_columns,
        "industries": industries,
        "person_location": [city, state, country],
        "company_location": [company_city, company_state, company_country],
        "desg_bucket": desg_bucket,
        "sample_length": sample_length,
        "min_emp": min_emp,
        "max_emp": max_emp,
        "additional_columns": additional_columns,
        "additional_req": additional_req,
        "people_per_company": people_per_company,
        "phone_codes": phone_codes,
        "currency": currency,
        "revenue_range": revenue_range,
    }


def remove_https(website: str) -> str:
    if "https://" in website:
        website = website.strip("https://")
    elif "http://" in website:
        website = website.strip("http://")

    return website.strip("/")


def get_exclusion(temp_file: BinaryIO) -> dict[str, list]:
    exclusion_dict: dict[str, list] = {"phone": [], "email": [], "website": []}

    temp_df = pd.ExcelFile(temp_file)
    if len(temp_df.sheet_names) >= 3 and "Exclusion" in temp_df.sheet_names:
        df = pd.read_excel(temp_file, sheet_name="Exclusion")
        df.columns = [column.lower() for column in df.columns]

        for column in list(df.columns):
            if "phone" in column:
                lst = df[column].dropna().to_list()
                exclusion_dict["phone"] = exclusion_dict["phone"] + lst
            if "email" in column:
                lst = df[column].dropna().to_list()
                exclusion_dict["email"] = exclusion_dict["email"] + lst
            if "website" in column:
                lst = df[column].dropna().to_list()
                exclusion_dict["website"] = exclusion_dict["website"] + lst

    exclusion_dict["website"] = list(
        map(lambda website: remove_https(website), exclusion_dict["website"])
    )

    return exclusion_dict


def validate_phone(phone_no: str, phone_codes: list[str]):
    phone_no = phone_no.replace(".0", "")
    if not phone_no.startswith("+"):
        phone_no = "+" + phone_no

    for phone_code in phone_codes:
        if phone_no.startswith(phone_code):
            phone_no = phone_no.replace(phone_code, "").strip()
            break

    return phone_no
