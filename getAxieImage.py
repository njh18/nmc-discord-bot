import json
import requests
import discord
from getAxieStatsParts import getAxieStatsParts

def getAxieImage(axieId,fighterClass):
  url = "https://graphql-gateway.axieinfinity.com/graphql"

  axie_url = "https://marketplace.axieinfinity.com/axie/" + str(axieId)
  embed = 0
  if(fighterClass=="Aquatic"):
    title = "Aqua - " + str(axieId)
    embed = discord.Embed(title = title, color = 0x00B8CE, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Beast"):
    title = "Beast - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xFFB812, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Bird"):
    title = "Bird - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xFF8BBD, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Bug"):
    title = "Bug - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xFF5341, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Dawn"):
    title = "Dawn - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xBECEFF, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Dusk"):
    title = "Dusk - " + str(axieId)
    embed = discord.Embed(title = title, color = 0x129092, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Mech"):
    title = "Mech - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xC6BDD4, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Plant"):
    title = "Plant - " + str(axieId)
    embed = discord.Embed(title = title, color = 0x6CC000, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  elif(fighterClass=="Reptile"):
    title = "Reptile - " + str(axieId)
    embed = discord.Embed(title = title, color = 0xDC8BE4, url=axie_url)
    # embed.add_field(name="Note", value="Click title to view axie in marketplace",inline=True)

  payload = json.dumps({
  "operationName": "GetAxieDetail",
  "variables": {
    "axieId": axieId
  },
  "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n image\n } \n } \n "
})
  headers = {
  'Content-Type': 'application/json'
}

  response = requests.request("POST", url, headers=headers, data=payload)
  axie_image = json.loads(response.text)['data']['axie']['image']
  embed.set_thumbnail(url=axie_image)

  stats_parts_list = getAxieStatsParts(axieId)
  
  counter = 0
  name_list = "| "
  card_list = "| "
  stat_list = "| "
  stat_value_list = "| "

  for statPart in stats_parts_list:
    if('name' in statPart):
      name_list += statPart['name']
      if(counter<3): name_list += " | "
      
    if('card' in statPart):
      card_list += statPart['card']
      if(counter<3): card_list += " | "
      counter+=1
    if('stat' in statPart):
      stat_list += statPart['stat'].upper()
      if(counter<3): stat_list += " | "
      
    if('value' in statPart):
      stat_value_list += str(statPart['value'])
      if(counter<3): stat_value_list += " | "
      counter+=1
    if(counter>=3):
      counter=0
 
  
  embed.add_field(name=name_list, value=card_list, inline=False)
  embed.add_field(name=stat_list, value=stat_value_list, inline=True)

  embed.set_footer(text="Click the title to view the axie in marketplace")

  return embed
##





