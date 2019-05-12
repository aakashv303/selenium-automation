import csv
def divideString(string): 
    substr_list = [string[0:5], string[5:10], string[10:15], string[15:20], string[20:25], string[-1]]
    return substr_list

def codeIsExists(string,csvfile):
	with open(csvfile, 'rt') as f:
	    reader = csv.reader(f, delimiter=',')
	    for row in reader:
	        for field in row:
	            if field == string:
	                return True
	    return False

def writeCSV(string,csvfile):
	file = open(csvfile, 'a')
	file.write(','+string)
	file.close()