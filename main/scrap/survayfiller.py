import os
import logging
import time
from selenium import webdriver

import config

WEB_DRIVER = config.WEB_DRIVER
SITE_URL = config.SITE_URL

def load_driver():
	driver = webdriver.Chrome(executable_path=os.path.join(WEB_DRIVER))

	return driver


def open_site(driver, url,text_list,typeID):
	# page 1
	driver.get(url)
	for index,value in enumerate(text_list):
		element = driver.find_element_by_id("CN{}".format(index+1))
		element.send_keys(value)
	driver.find_element_by_id('NextButton').click()

	while driver.find_elements_by_id('NextButton'):
		radiobtn_list = driver.find_elements_by_class_name('radioBranded')
		row_list = driver.find_elements_by_class_name('InputRowOdd')
		checkbox_list = driver.find_elements_by_class_name('checkboxBranded')
		order_page = [ele for ele in driver.find_elements_by_class_name('FNSText') if ele.text == "Please select your order type:"]
		if radiobtn_list and len(radiobtn_list) < 3 and len(row_list) < 2:
			radiobtn_list[-1].click()

		elif order_page:
			order_option = driver.find_elements_by_class_name('Opt{}'.format(typeID))[0]
			order_option.find_elements_by_class_name('radioBranded')[0].click()
		elif radiobtn_list and len(row_list) < 2:
			radiobtn_list[0].click()

		elif row_list:
			radiobtns = row_list
			for row in radiobtns:
				row.find_element_by_class_name('radioBranded').click()
			radiobtns = driver.find_elements_by_class_name('InputRowEven')
			for row in radiobtns:
				row.find_element_by_class_name('radioBranded').click()

		elif checkbox_list:
			checkbox_list[3].click()
			checkbox_list[1].click()
			checkbox_list[4].click()

		elif driver.find_elements_by_xpath("//select[@name='R022000']/option[text()='Female']"):
			driver.find_element_by_xpath("//select[@name='R022000']/option[text()='Female']").click()
			driver.find_element_by_xpath("//select[@name='R023000']/option[text()='18 to 24']").click()
			driver.find_element_by_xpath("//select[@name='R000206']/option[text()='Yes']").click()
			driver.find_element_by_xpath("//select[@name='R024000']/option[text()='$25,000 to $44,999']").click()
			driver.find_element_by_xpath("//select[@name='R025000']/option[text()='Asian']").click()

		if driver.find_elements_by_xpath("//div[@id='WaitScreen']"):
			time.sleep(2)
		driver.find_element_by_id('NextButton').click()

	if driver.find_element_by_class_name('ValCode').is_displayed():
		coupon = driver.find_element_by_class_name('ValCode').text
		return coupon


def automate(prox_driver, text_list,typeID):
	# driver = load_driver()
	coupon = open_site(prox_driver,SITE_URL,text_list,typeID)

	return coupon
