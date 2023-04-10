import pandas as pd
from typing import BinaryIO
from app.qc_automation.bucketing import load_bucket

def splitByComma(string: str) -> list:
    if str(string) != "nan":
        return list(map(lambda x: x.strip().lower(), string.split(",")))
    return []

def get_constraints(temp_file: BinaryIO) -> dict:
    df = pd.read_excel(temp_file)
    df.columns = [column.lower() for column in list(df.columns)]

    required_columns = ["first name", "company", "primary phone", "work email"]

    industries = splitByComma(df.loc[0, "industry"])

    city = []
    state = []
    country = []
    if str(df.loc[0, "city"]).lower() != "n/a":
        city = splitByComma(df.loc[0, "city"])
    if str(df.loc[0, "state"]).lower() != "n/a":
        state = splitByComma(df.loc[0, "state"])
    if str(df.loc[0, "country"]).lower() != "n/a":
        country = splitByComma(df.loc[0, "country"])

    designation = []
    if str(df.loc[0, "designation"]).lower() != "n/a":
        BUCKET = load_bucket()
        designation = splitByComma(df.loc[0, "designation"])
        desg_bucekt = []
        for desg in designation:
            if desg in BUCKET:
                desg_bucekt += BUCKET[desg]
            else:
                desg_bucekt.append(desg)
        desg_bucekt = list(map(lambda x: x.lower(), desg_bucekt))

    quantity = df.loc[0, "quantity"]
    sample_length = 0
    if quantity:
        sample_length = int(quantity)

    num_emp = df.loc[0, "# employees"]
    if str(num_emp) != "n/a":
        min_emp, max_emp = map(int, num_emp.split("-"))
    else:
        min_emp, max_emp = 0, 500000

    additional_column_value = str(df.loc[0, "additional columns"]).lower()
    if additional_column_value != "n/a":
        additional_columns = splitByComma(df.loc[0, "additional columns"])
        additional_columns = list(map(lambda x: x.lower(), additional_columns))

        df.columns = map(str.lower, df.columns)
        additional_req = {}
        for column in additional_columns:
            additional_req[column] = splitByComma(df.loc[0, column])
    else:
        additional_columns = []
        additional_req = {}

    people_per_company = df.loc[0, "number of people/company"]

    return {
        "required_columns": required_columns,
        "industries": industries,
        "city": city,
        "state": state,
        "country": country,
        "desg_bucket": desg_bucekt,
        "sample_length": sample_length,
        "min_emp": min_emp,
        "max_emp": max_emp,
        "additional_columns": additional_columns,
        "additional_req": additional_req,
        "people_per_company": people_per_company,
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
    if len(temp_df.sheet_names) >= 3 and 'Exclusion' in temp_df.sheet_names:
        df = pd.read_excel(temp_file, sheet_name='Exclusion')
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

def validate_phone(phone):
    if not phone.startswith("+"):
        phone = "+" + phone
    return phone.replace(".0","").replace("+91", "").strip()