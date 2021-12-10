import requests
import os
import json
import discord
from Builder.roninAddConverter import roninAddConverter
from replit import db
import sys

def getGuildAverageSLP(min_slp):
  
	title = "Guild : Scholars with Average SLP of " + str(min_slp) + " and below."
	embed = discord.Embed(title =  title, color = 0xff8585)
	clans = ['oasis', 'lunar', 'kopi', 'sol']
	clan_emojis = {'oasis' : '\N{Palm Tree}', 'lunar' : '\N{Last Quarter Moon with Face}','kopi' : '\N{Hot Beverage}','sol':'\N{Glowing Star}'}
	embed_list = []
  
	roninAddDb = json.loads(db.get_raw("roninAdd"))
	embed_count = 0
	try:
		for clan in clans:
			scholarDb = roninAddDb[clan]
			for user in scholarDb:
    #get 0x
				scholarRonin = roninAddConverter(user["scholarRonin"]) 
				url = "https://axie-infinity.p.rapidapi.com/get-update/" + scholarRonin +"?id=" + scholarRonin

				headers = {
			  	'x-rapidapi-host': 'axie-infinity.p.rapidapi.com',
			  	'x-rapidapi-key': os.environ['x-rapidapi-key']
			  }

				response = requests.request("GET", url, headers=headers, data={})

				json_data = json.loads(response.text)
        
				thename = "???" if json_data['leaderboard']['name'] == None else str(json_data['leaderboard']['name'])
				print(str(thename) + ' - Average SLP : ' + str(json_data['slp']['average']))
				if thename is None:
					break 
				elif json_data['slp']['average'] == None:
					continue
				elif json_data['slp']['average'] <= int(min_slp):
					print('added to list')
					avg = json_data['slp']['average']
					ytdSlp = json_data['slp']['yesterdaySLP']
					mmr = json_data['leaderboard']['elo']
					embed.add_field(name = thename, value = str(clan_emojis[clan])+ " MMR: " + str(mmr) + ", Yesterday SLP : " + str(ytdSlp) + ", Average SLP : " + str(avg),inline=False)
					embed_count += 1
					if(embed_count==25):
						print('start new list')
						embed_count = 0
						embed_list.append(embed)
						embed = discord.Embed(title =  title, color = 0xff8585)
		if(len(embed_list)!=25):
			embed_list.append(embed)
		return embed_list
	except:
		print(value=sys.exc_info()[0])
		embed=discord.Embed(title="Oops!", color = discord.Color.light_gray())
		embed.add_field(name="Error", value=sys.exc_info()[0])
		return embed
      # print("sys.exc_info()[0], "occurred.")
		


