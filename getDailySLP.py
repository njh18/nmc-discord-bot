import requests
import os
import json
import discord

def getDailySLP(roninAdd):

	roninAdd = roninAdd.replace("ronin:","0x")
	print(roninAdd)
	url = "https://axie-infinity.p.rapidapi.com/get-update/" + roninAdd +"?id=" + roninAdd

	payload={}
	headers = {
		'x-rapidapi-host': 'axie-infinity.p.rapidapi.com',
		'x-rapidapi-key': os.environ['x-rapidapi-key']
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	json_data = json.loads(response.text)

	thename = json_data['leaderboard']['name']

	if thename is None:
			return discord.Embed(title = "Cannot Find User", color = discord.Color.red())
	else:
		todaySlp = json_data['slp']['todaySoFar']
		ytdSlp = json_data['slp']['yesterdaySLP']
		totalSlp = json_data['slp']['total']
		mmr = json_data['leaderboard']['elo']

		embed = discord.Embed(title = "Today's Updates", color = discord.Color.red())
		embed.set_author(name=thename)
		embed.add_field(name =  "Today SLP", value = todaySlp,inline=True)
		embed.add_field(name =  "Ytd SLP", value = ytdSlp,inline=True)
		embed.add_field(name =  "Total SLP", value = totalSlp,inline=True)
		embed.add_field(name =  "MMR", value = mmr,inline=True)
		
		return embed
