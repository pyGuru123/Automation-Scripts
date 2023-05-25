# Chrome version 113

import sys
import time
import json
import random
import selenium
from loguru import logger
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

def login_apollo(email_id: str, pwd: str) -> str:
	wait = WebDriverWait(driver, 20)
	form = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "form")))
	if form:
		email = driver.find_element(By.NAME, "email")
		password = driver.find_element(By.NAME, "password")

		email.clear()
		email.send_keys(email_id)
		password.send_keys(pwd)
		form.submit()

		wait = WebDriverWait(driver, 20)
		profile_btn = driver.find_element(By.CLASS_NAME, "zp_zUY3r")
		if profile_btn:
			return "success"

	return "failed"


def logout_apollo() -> None:
	menu_buttons = driver.find_elements(By.CLASS_NAME, "zp-button")
	for button in menu_buttons:
		if button.text == "MA":
			button.click()
			break

	time.sleep(1)
	logout_div = driver.find_element(By.CLASS_NAME, "apollo-icon-log-out")
	logout_div.click()
	print("logged out")


def load_search_page():
	driver.get("https://app.apollo.io/#/onboarding/checklist")


def search_person(string):
	try:
		wait = WebDriverWait(driver, 10)
		input_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='provider-mounter']/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/input[1]")))
		input_box.send_keys(Keys.CONTROL, 'a')
		input_box.send_keys(Keys.BACKSPACE)
		input_box.send_keys(string)	
		wait = WebDriverWait(driver, 10)
		recommended = [wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='provider-mounter']/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]")))]
		if len(recommended) > 0:
			if recommended[0].text != "Job Titles": 
				recommended[0].click()
				wait = WebDriverWait(driver, 15)
				try:
					div = [wait.until(EC.visibility_of_element_located((By.ID, "general_information_card")))]
					if len(div) > 0:
						return "success"
				except selenium.common.exceptions.TimeoutException:
					load_search_page()

		return "failed"

	except selenium.common.exceptions.TimeoutException:
		return "failed"

def get_name():
	return driver.find_element(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").text

def get_designation_company():
	profile_info = driver.find_element(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]")
	return profile_info.text.split("\n")

def get_linkedin():
	urls = driver.find_elements(By.TAG_NAME, "a")
	for url in urls:
		if url.get_attribute("href") is not None:
			if "http://www.linkedin.com/in/" in url.get_attribute("href"):
				return url.get_attribute("href")

def get_phone():
	try:
		phone_no = ""
		get_phone_number = driver.find_elements(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/span[1]/a[1]")
		if len(get_phone_number) > 0:
			get_phone_number[0].click()
			wait = WebDriverWait(driver, 25)
			phone = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]/span[1]")))
			phone_no = phone.text
		else:
			phones = driver.find_elements(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/a[1]/span[1]")
			if len(phones) > 0:
				for phone in phones:
					if phone.text:
						return phone.text
				# phone_no = phones[0].text
				# if not phone_no and len(phones) > 1:
				# 	return phones[1].text
	except:
		print("Phone Doesn't exist")


def get_email():
	try:
		out_of_credits = driver.find_element(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]")
		out_of_credits.click()
		WebDriverWait(driver, 3)
		buttons = driver.find_elements(By.TAG_NAME, "button")
		for button in buttons:
			if "Re-verify" in button.text:
				button.click()
				break

		time.sleep(1)
		wait = WebDriverWait(driver, 15)
		email_label = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]")))
		return email_label.text		
	except Exception as e:
		logger.info("Email Doesn't exist")


def get_contact_details():
	name, designation, company, email, phone = [""] * 5

	time.sleep(2)
	name = get_name()
	designation, company = get_designation_company()
	linkedin_url = get_linkedin()

	try:
		wait = WebDriverWait(driver, 2)
		try:
			access_deatail_btn = driver.find_element(By.CLASS_NAME, "apollo-icon-cloud-download")
			access_deatail_btn.click()
		except Exception as e:
			logger.error(e)
			access_details_btn = driver.find_element(By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/button[1]")
			access_details_btn.click()
		wait = WebDriverWait(driver, 25)
		print("fetching details")
		add_phone_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='general_information_card']/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/button[1]")))
	except:
		print("profile already checked")

	phone = get_phone()
	email = get_email()

	return {
		"name" : name,
		"designation" : designation,
		"company" : company,
		"email" : email,
		"phone" : phone,
		"linkedin_url" : linkedin_url
	}


def apollo_search_single(query):
	status = search_person(query)
	print(status, query)
	if status == "success":
		data = get_contact_details()
		return data

	return {}

def apollo_search_bulk(queries):
	json_data = {}
	for query in queries:

		start_time = time.time()
		data = apollo_search_single(query)
		end_time = time.time()
		print(end_time - start_time)

		json_data[query] = data
		time.sleep(random.randint(4, 8))

	return json_data


if __name__ == "__main__":
	queries = [
		# "Linas Beliūnas Flutterwave",
		# "Veenu Chopra WalkingTree Resources Pvt. Ltd"
		# "Tejas Yevalkar GS Lab",
		"Naveen Suppala ICE",
		# "Alexander Gursky Indon International",
	]

	driver = webdriver.Chrome(service=service, options=chrome_options)
	driver.maximize_window()

	driver.get("https://app.apollo.io/#/login")
	login_status = login_apollo(email_id, pwd)
	if login_status == "success":
		load_search_page()
		json_data = apollo_search_bulk(queries)
		with open("contacts_apollo2.json", "w") as json_file:
		    json.dump(json_data, json_file)
		# print(json_data)
		time.sleep(3)
		logout_apollo()