import requests
import os
import json
import discord
from replit import db

def getClanSLP(clan):

	# Initialise the embeded
	if clan == "Oasis":
		color = discord.Color.blue()
	elif clan == "Lunar":
		color = discord.Color.gold()
	elif clan == "Kopi":
		color = discord.Color.dark_purple()
	elif clan == "Sol":
		color = discord.Color.red()

	embed = discord.Embed(title = clan +  " clan's Daily Updates", color = color)

	roninAddDb = json.loads(db.get_raw("roninAdd"))[clan]

	for user in roninAddDb:
		roninAdd = user["eth"].replace("ronin:","0x")
		url = "https://axie-infinity.p.rapidapi.com/get-update/" + roninAdd +"?id=" + roninAdd

		payload={}
		headers = {
			'x-rapidapi-host': 'axie-infinity.p.rapidapi.com',
			'x-rapidapi-key': os.environ['x-rapidapi-key']
		}

		response = requests.request("GET", url, headers=headers, data=payload)

		json_data = json.loads(response.text)
		print(json_data)
		thename = json_data['leaderboard']['name']

		if thename is None:
				break 
		else:
			todaySlp = json_data['slp']['todaySoFar']
			ytdSlp = json_data['slp']['yesterdaySLP']
			totalSlp = json_data['slp']['total']
			mmr = json_data['leaderboard']['elo']

		embed.add_field(name = thename, value = "Today's SLP: " + str(todaySlp) + ", Ytd SLP: " + str(ytdSlp) + ", Total SLP: " + str(totalSlp) + ", MMR: " + str(mmr) ,inline=False)

	return embed


