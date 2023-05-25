# Chrome version 113

import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "/chromedriver.exe"
service = Service(PATH)

email_id = ""
pwd = "" 

chrome_options = Options()
chrome_options.add_argument("--incognito")

search_page_endpoint = "https://rocketreach.co/person?start=1&pageSize=10&link="

def login_rr(email_id, pwd):
	time.sleep(5)

	form = driver.find_element(By.ID, "user-signup")
	email = driver.find_element(By.NAME, "email")
	password = driver.find_element(By.NAME, "password")

	email.clear()
	email.send_keys(email_id)
	password.send_keys(pwd)
	form.submit()

	wait = WebDriverWait(driver, 20)

	page_source = driver.page_source
	if "We don't recognize this device or location!" in page_source:
		verification_btn = driver.find_element(By.CLASS_NAME, "btn-pronounced")
		verification_btn.click()
		return "device not recognized"
	elif "Bulk Lookups" in page_source:
		return "success"
	else:
		return "timeout"

def check_login_status(email_id, pwd):
	login_status = login_rr(email_id, pwd)
	if login_status == "timeout":
		login_status = check_login_status(email_id, pwd)
	elif login_status == "device not recognized":
		sys.exit(0)
	
	return login_status


def logout_rr():
	account_dropdown = driver.find_element(By.CLASS_NAME, "account-info")
	account_dropdown.click()
	time.sleep(1)
	logout = driver.find_element(By.CLASS_NAME, "fa-sign-out")
	logout.click()
	print("logged out")


def search_single(linkedin_url):
	url = search_page_endpoint + linkedin_url.replace("/", "%2F")
	driver.get(url)
	# time.sleep(5)

	wait = WebDriverWait(driver, 15)
	try:
		info = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-results-list-item--0")))
	except:
		wait = WebDriverWait(driver, 10)
		info = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-results-list-item--0")))

	if info:
		try:
			get_contact = info.find_element(By.CLASS_NAME, "fa-user-plus")
			get_contact.click()
			time.sleep(15)
		except:
			print("already in contacts")

		try:
			name = driver.find_element(By.CLASS_NAME, "profile-directive-column-name__info").text
			name, designation = name.split("\n")
		except:
			name, designation = "", ""

		try:
			location = driver.find_element(By.CLASS_NAME, "profile-directive-column-info-wpr").text.split("\n")[0]
		except:
			location = ""

		try:
			company = driver.find_element(By.CLASS_NAME, "rr-popover-link").text.split("\n")[0]
		except:
			company = ""

		try:
			contacts = driver.find_elements(By.CLASS_NAME, "contact-list__entry__link")
			email, phone = "", ""
			email = contacts[0].text.split("\n")[0]
			for contact in contacts:
				if sum(1 for char in contact.text if char.isdigit()) >= 10:
					phone = contact.text
					break
		except:
			email, phone = "", ""

		return {
			"name" : name,
			"designation" : designation,
			"location" : location,
			"company" : company,
			"email": email,
			"phone" : phone
		}

def search_bulk(linkedin_urls):
	data_dict = {}
	for linkedin_url in linkedin_urls:
		time.sleep(5)
		data = search_single(linkedin_url)
		print(data)
		data_dict[linkedin_url] = data

	return data_dict


if __name__ == "__main__":
	linkedin_urls = ["https://www.linkedin.com/in/malharlakdawala/",
					 "https://www.linkedin.com/in/raveenbeemsingh/",
					 "https://www.linkedin.com/in/sonakshi-pratap/",
					 "https://www.linkedin.com/in/karan-gupta707/",
					 "https://www.linkedin.com/in/yash-96/"
					]

	driver = webdriver.Chrome(service=service, options=chrome_options)

	driver.get("https://rocketreach.co/login")
	login_status = check_login_status(email_id, pwd)
	if login_status == "success":
		json_data = search_bulk(linkedin_urls)
		print(json_data)
		with open("contacts_rr.json", "w") as json_file:
		    json.dump(json_data, json_file)

	time.sleep(3)
	logout_rr()
	driver.quit()

# return {
        #         "name" : data["name"],
        #         "company" : data["current_employer"],
        #         "designation" : data["current_title"],
        #         "location" : data["location"],
        #         "work_email" : data["current_work_email"],
        #         "recommended_email" : data["recommended_email"],
        #         "phones" : [phone["number"] for phone in data["phones"]]
        #     }
