import requests
import os
import json
import discord
from getUpdateRapidApi import getUpdateRapidApi

def getDailySLP(roninAdd):
	
	json_data = json.loads(getUpdateRapidApi(roninAdd))

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
