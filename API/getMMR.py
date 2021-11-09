import requests
import os
import json
import discord
from API.getUpdateRapidApi import getUpdateRapidApi

def getMMR(roninAdd):
  try:
    json_data = json.loads(getUpdateRapidApi(roninAdd))
    thename = json_data['leaderboard']['name']

    if thename is None:
        return discord.Embed(title = "Cannot Find User", color = discord.Color.red())
    else:
      mmr = json_data['leaderboard']['elo']
      embed = discord.Embed(title = "Account Details", color = discord.Color.orange())
      if(roninAdd=="ronin:c841df9a10676269335864da9a7392240e535510"):
        embed.add_field(name="Bow the f*ck down because your boss's MMR is", value="9999")
        embed.set_footer(text='Know your f*cking place, ant. 🐜')
        embed.set_thumbnail(url="https://i.ibb.co/QQTGVNs/Mask-Group-1.png")
        return embed
      embed.add_field(name="Your current MMR is", value=mmr)
      return embed
  except:
    embed = discord.Embed(title = "SLP Information not retrieved! 😭")
    embed.add_field(name = "Network Error", value = "There seems to be problem with Axie's server at the moment. Please check back in abit.")
    return embed
