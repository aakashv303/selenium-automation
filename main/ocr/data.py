import pytesseract
import config

TESSERACT_DRIVER = config.TESSERACT_DRIVER
def extract_data(image):
	pytesseract.pytesseract.tesseract_cmd = TESSERACT_DRIVER
	return pytesseract.image_to_string(image,lang='enm')