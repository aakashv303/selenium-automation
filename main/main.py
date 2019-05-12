import os
import csv
import logging
from time import time


import utils
import config
from error import error_logs
from ocr.ocr import image_scan
from hideIP.proxy import maskIP

DINE_IN_UPLOAD_PATH = config.DINE_IN_UPLOAD_PATH
DRIVE_THRU_UPLOAD_PATH = config.DRIVE_THRU_UPLOAD_PATH
CARRY_OUT_UPLOAD_PATH = config.CARRY_OUT_UPLOAD_PATH
WEB_DRIVER = config.WEB_DRIVER
CODE_CSV = config.CODE_CSV

logger = error_logs.get_logger(__name__)
def main():
	# list of images in text detection folder
	DINE_IN_files = os.listdir(DINE_IN_UPLOAD_PATH)
	DRIVE_THRU_files = os.listdir(DRIVE_THRU_UPLOAD_PATH)
	CARRY_OUT_files = os.listdir(CARRY_OUT_UPLOAD_PATH)
	for file in DINE_IN_files:
		image = os.path.join(DINE_IN_UPLOAD_PATH, file)
		text = image_scan(image)
		process_survay(text,1,file) # 0 = order_type DINE_IN
	for file in DRIVE_THRU_files:
		image = os.path.join(DRIVE_THRU_UPLOAD_PATH, file)
		text = image_scan(image)
		process_survay(text,2,file) # 1 = order_type DINE_THRU
	for file in CARRY_OUT_files:
		image = os.path.join(CARRY_OUT_UPLOAD_PATH, file)
		text = image_scan(image)
		process_survay(text,3,file) # 2 = order_type CARRY_OUT
		
		

def process_survay(text,typeID,file):
	if utils.codeIsExists(text,CODE_CSV):
		logger.info("detected code for {}: {} is already submitted".format(file,text))
		return True
	# devide text into chunk of 5 numbers
	text_partition = utils.divideString(text)

	# automate task of survay
	coupon_text, proxy = maskIP(text_partition,typeID)


	logger.info("detected code for {}: {}, {} (proxy={})".format(file,text,coupon_text,proxy))
	utils.writeCSV(text,CODE_CSV)
	return True

if __name__ == '__main__':
	main()