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
      if(roninAdd=="ronin:c841df9a10676269335864da9a7392240e535510"):
        embed.add_field(name="Bow the f*ck down because your boss's MMR is", value="9999")
        embed.set_footer(text='Know your f*cking place, ant. 🐜')
        embed.set_thumbnail(url="https://i.ibb.co/QQTGVNs/Mask-Group-1.png")
        return embed
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
