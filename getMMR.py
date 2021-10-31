import requests
import os
import json
import discord
from getUpdateRapidApi import getUpdateRapidApi

def getMMR(roninAdd):
  try:
    json_data = json.loads(getUpdateRapidApi(roninAdd))
    thename = json_data['leaderboard']['name']

    if thename is None:
        return discord.Embed(title = "Cannot Find User", color = discord.Color.red())
    else:
      mmr = json_data['leaderboard']['elo']

      embed = discord.Embed(title = "Account Details", color = discord.Color.orange())
      # embed.set_author(name=thename)
      # today = date.today()
      # yesterday = today - datetime.timedelta(day=1)
      # today = "Today (" + str(datetime.now().strftime("%b-%d")) + ")"
      # ytd = "Yesterday (" + str((datetime.now() - timedelta(1)).strftime("%b-%d")) + ")"
      # print(today-1)
      # print(today)
      # print(yesterday)
      # ytd = "Yesterday" + date.yesterday().strftime("%b-%d")
      # random_pic_index = randint(0,len(img_list)-1)
      embed.add_field(name="Your current MMR is", value=mmr)

      # embed.set_thumbnail(url = img_list[random_pic_index])
      # embed.add_field(name =  "MMR", value = mmr,inline=True)
      
      return embed
  except:
    embed = discord.Embed(title = "SLP Information not retrieved! 😭")
    embed.add_field(name = "Network Error", value = "There seems to be problem with Axie's server at the moment. Please check back in abit.")
    return embed
