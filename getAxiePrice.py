import os
import json
import requests
from replit import db
import discord
from datetime import datetime

def getAxiePrice(buildName):

	filterData = json.loads(db.get_raw("filters"))
	f = open('GetAxieBriefList.json')

	payload = json.load(f)
	payload["variables"]["criteria"] = filterData[buildName]["criteria"]

	url = os.environ["GRAPHQL"]

	headers = {
	'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

	if response.text == "Bad Request":
		return "Bad Request Sent"
	else:
		json_data = json.loads(response.text)
		
		url = filterData[buildName]["url"]

		embed = discord.Embed(title ="The current prices for " + buildName + " build are: (Click Here to go to 	marketplace\n\n", url = url, color = discord.Color.random())

		totalCostEth = 0
		totalCostUsd = 0
		count = 1
		for axie in json_data["data"]["axies"]["results"]:
			embed.add_field(name ="%d. Price: %.4f ETH / US$ %.2f"%(count,float(axie["auction"]["currentPrice"][0:-14])/10000, float(axie["auction"]["currentPriceUSD"])), value = "Link: https://marketplace.axieinfinity.com/axie/%s/" %(axie['id']),inline=False)

			# To insert into database
			count +=1
			totalCostEth += float(axie["auction"]["currentPrice"][0:-14])/10000
			totalCostUsd += float(axie["auction"]["currentPriceUSD"])

		# now = datetime.now()
		# theList = db["prices"][buildName].value
		# print(theList)
		# theList.append([now,totalCostEth/count,totalCostUsd/count])
		# print(theList)
		# db["prices"][buildName] = (theList)
		# print(db["prices"])
		
		return embed


