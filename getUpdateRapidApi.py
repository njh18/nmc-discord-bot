import requests
import os

def getUpdateRapidApi(roninAdd):

	roninAdd = roninAdd.replace("ronin:","0x")
	print(roninAdd)
	url = "https://axie-infinity.p.rapidapi.com/get-update/" + roninAdd +"?id=" + roninAdd

	payload={}
	headers = {
		'x-rapidapi-host': 'axie-infinity.p.rapidapi.com',
		'x-rapidapi-key': os.environ['x-rapidapi-key']
	}

	response = requests.request("GET", url, headers=headers, data=payload)
		
	return response.text
