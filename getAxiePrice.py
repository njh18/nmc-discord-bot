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

		embed = discord.Embed(title ="The average floor prices for " + buildName + " build are: \n\n", url = url, color = discord.Color.random())

		totalCostEth = 0
		totalCostUsd = 0
		count = 1
		for axie in json_data["data"]["axies"]["results"]:
			# To insert into database
			count +=1
			totalCostEth += float(axie["auction"]["currentPrice"][0:-14])/10000
			totalCostUsd += float(axie["auction"]["currentPriceUSD"])

		embed.add_field(name ="Eth Cost", value = round(totalCostEth/count,5) ,inline=True)
		embed.add_field(name ="Usd Cost", value = round(totalCostUsd/count,3) ,inline=True)

		# add data into database
		now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		db["prices"][buildName].append([now,totalCostEth/count,totalCostUsd/count])
	
		return embed


