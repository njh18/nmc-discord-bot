import os
import json
import requests

def getAxiePrice(criteria):
	url = os.environ["GRAPHQL"]

	f = open('GetAxieBriefList.json')

	payload = json.load(f)
	payload["variables"]["criteria"] = criteria

	headers = {
	'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

	if response.text == "Bad Request":
		return "Bad Request Sent"
	else:
		json_data = json.loads(response.text)
		msg = "The current prices for requested axies are: \n\n"
		count = 1
		for axie in json_data["data"]["axies"]["results"]:
			theString = "%d. Price: %.4f ETH / US$ %.2f Link: https://marketplace.axieinfinity.com/axie/%s/" %(count,float(axie["auction"]["currentPrice"][0:-14])/10000, float(axie["auction"]["currentPriceUSD"]),axie['id'])
			msg = msg + theString + "\n"
			count +=1
		return msg


