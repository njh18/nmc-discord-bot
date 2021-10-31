# Import required modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import os
import json
import pandas as pd

def loadDb():
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']

	my_secret = json.loads(os.environ['GOOGLE-DRIVE-API-KEY'])

	# Assign credentials ann path of style sheet
	creds = ServiceAccountCredentials.from_json_keyfile_dict(my_secret, scope)
	client = gspread.authorize(creds)
	sheet = client.open("Scholar Details").sheet1

	result = sheet.get_all_records()

	df = pd.DataFrame()
	for item in result:
		df = df.append(item,ignore_index=True)
	
	return df