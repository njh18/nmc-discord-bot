import requests
import os
import json
import discord
from API.getUpdateRapidApi import getUpdateRapidApi
from datetime import datetime, timedelta
from replit import db
from random import random,randint

def getDailySLP(roninAdd):
  try:
    json_data = json.loads(getUpdateRapidApi(roninAdd))

    clans = ['oasis', 'kopi', 'lunar', 'sol', 'singapore']
    thename = 0
    
    for clan in clans: 
      roninAddDb = json.loads(db.get_raw("roninAdd"))[clan]
      for scholar in roninAddDb:
        if scholar["scholarRonin"] == roninAdd:
          thename = scholar["name"]
          print(thename + " - scholar found")
    
    print(thename)
    # thename = json_data['leaderboard']['name']

    print(thename)
    if thename == 0:
        return discord.Embed(title = "Cannot Find User", color = discord.Color.red())
    else:
      img_list = ['https://cdn.substack.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fbac8205a-83c0-4b6d-8002-ed62f105ffcf_128x127.png','https://chimeratribune.com/wp-content/uploads/2020/11/Asset-18.png','https://cdn.substack.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fa92f32d1-736b-480f-89f2-975312de48fb_102x128.png','https://cdn.substack.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F71cb79f2-fc94-4c5f-adee-55049b9c4a49_324x298.png','https://lh6.googleusercontent.com/e-uyw8Vg6iOCR7YK4s8Riy4Mwdug4OW3IwE9NGvCPMBVJqWpTm-oMBlhJw9rA-3KfNIr23Cv-KRiuN9Y0-HQGXsE66XyL6C0JnvMRhTk5yTPoZE27-F9Fa6XOhHZaXcAOMTjX_5U']

      todaySlp = json_data['slp']['todaySoFar']
      ytdSlp = json_data['slp']['yesterdaySLP']
      avgSlp = json_data['slp']['average']
      totalSlp = json_data['slp']['total']
      # mmr = json_data['leaderboard']['elo']

      embed = discord.Embed(title = "Account $SLP Status", color = discord.Color.red())
      embed.set_author(name=thename)
      # today = date.today()
      # yesterday = today - datetime.timedelta(day=1)
      today = "Today (" + str(datetime.now().strftime("%b-%d")) + ")"
      ytd = "Yesterday (" + str((datetime.now() - timedelta(1)).strftime("%b-%d")) + ")"
      # print(today-1)
      # print(today)
      # print(yesterday)
      # ytd = "Yesterday" + date.yesterday().strftime("%b-%d")
      random_pic_index = randint(0,len(img_list)-1)
      print(json_data['leaderboard'])
      embed.add_field(name = "Average SLP", value = avgSlp, inline=True)

    
      embed.add_field(name = "⠀", value = "⠀",inline=True)
      embed.add_field(name =  "Total SLP", value = totalSlp,inline=True)
      embed.add_field(name = today, value = todaySlp,inline=True)
      embed.add_field(name = "⠀", value = "⠀",inline=True)
      embed.add_field(name =  ytd, value = ytdSlp,inline=True)

      embed.set_thumbnail(url = img_list[random_pic_index])
      # embed.add_field(name =  "MMR", value = mmr,inline=True)
      
      return embed
  except:
    embed = discord.Embed(title = "SLP Information not retrieved! 😭")
    embed.add_field(name = "Network Error", value = "There seems to be problem with Axie's server at the moment. Please check back in abit.")
    return embed
