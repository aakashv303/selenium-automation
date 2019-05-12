import os
import cv2
import argparse
import pytesseract

from PIL import Image

import cv2
from .data import extract_data

def image_scan(path):
	
	SIZE = 2.2
	MAXSIZE = 0.3 # max size ratio if resolution is more than 800px
	#  read image from local
	image = cv2.imread(path)
	# height, width = image.shape[:2]

	# image denoising and enhancing
	# img = cv2.resize(img,None,fx=SIZE,fy=SIZE,interpolation=cv2.INTER_CUBIC)
	# _,th = cv2.threshold(img,0,255,cv2.THRESH_TRUNC+cv2.THRESH_OTSU)
	# cv2.imwrite(crop_path,th)

	text = extract_data(path)
	text = (text).encode("utf-8").decode('ascii', 'ignore')
	print('Detected data:\n',text)

	return text.split('\n')[-1]
