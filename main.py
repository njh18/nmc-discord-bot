import os
import discord
import requests
from replit import db
import json


client = discord.Client();
bot_token = os.environ['TOKEN']

def get_quote():
	url = "https://graphql-gateway.axieinfinity.com/graphql"

	payload = json.dumps({
		"operationName": "GetAxieBriefList",
		"variables": {
			"from": 0,
			"size": 10,
			"sort": "PriceAsc",
			"auctionType": "Sale",
			"criteria": {}
		},
		"query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
		})

	headers = {
	'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	json_data = json.loads(response.text)
	total_results = json_data["data"]["axies"]["total"]
	return total_results


def update_presets(payload):
	return
	


# when bot is ready to be use
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

	msg = message.content
	if message.author == client.user:
		return
	
	if msg.startswith('$get-axie'):
		quote = get_quote()
		await message.channel.send(quote)


client.run(bot_token)

