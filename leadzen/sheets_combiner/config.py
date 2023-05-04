import pandas as pd

def get_all_apollo_columns() -> list[str]:
    return ["First Name", "Last Name", "Title", "Company",
       "Company Name for Emails", "Email", "Phone No ", "# Employees",
       "Industry", "Keywords", "Person Linkedin Url", "Website",
       "Company Linkedin Url", "Facebook Url", "Twitter Url", "City", "State",
       "Country", "Company Address", "Company City", "Company State",
       "Company Country", "Technologies", "Annual Revenue", "Total Funding",
       "Latest Funding", "Latest Funding Amount", "Last Raised At"]

def get_required_apollo_columns() -> list[str]:
    return ["First Name", "Last Name", "Title", "Company", "Primary Phone",
        "Email", "# Employees", "Industry", "Person Linkedin Url",
        "Website", "Company Linkedin Url", "City", "State", "Country",
        "Company Address", "Company City", "Company State", "Company Country", "Revenue"]

def apollo_renamed_columns() -> dict[str, str]:
    return {
        "Phone No " : "Primary Phone",
        "Annual Revenue" : "Revenue"
    }

def rocket_renamed_columns() -> dict[str, str]:
    return {
        "title" : "Title",
        "company_name" : "Company",
        "linkedin_url" :  "Person Linkedin Url",
        "emails" : "Email",
        "phone_no's" : "Primary Phone",
        "industry" : "Industry"
    }

def sn_renamed_columns() -> dict[str, str]:
    return {
        "firstName" : "First Name",
        "lastName" : "Last Name",
        "title" : "Title",
        "linkedinProfileUrl" : "Person Linkedin Url",
        "companyUrl" : "Company Linkedin Url",
        "companyName" : "Company"
    }

def sheet_names(file):
    df = pd.ExcelFile(file)
    return sorted(list(df.sheet_names))