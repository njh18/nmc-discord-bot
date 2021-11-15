import discord
from API.getLeaderboard import getLeaderboard
from API.getRecentTeam import getRecentTeam

async def leaderboard(message):
  offset = 1
  limit = 2
  print(len(message.content.split(' ')))
  if (len(message.content.split(' ')) > 1):
      params = message.content.split("$leaderboard ", 1)[1]
      offset = int(params.split(',')[0]) - 1
      limit = params.split(',')[1]
  rank = offset + 1

  # getAxieImage embed format
  # for ranker in getLeaderboard(offset,limit):
  # 	await message.channel.send("Rank " + str(rank) + "\n " + "https://axie.zone/profile?ron_addr=" + str(ranker), embed=None)
  # 	for axie in getRecentTeam(ranker):
  # 		await message.channel.send(embed = getAxieImage(axie['id'],axie['class']))
  # 	rank += 1

  embed = 0
  axie_part = ''
  axie_stat = ''
  for ranker in getLeaderboard(offset, limit):
      embed = discord.Embed(title="Rank " + str(rank),
                            url="https://axie.zone/profile?ron_addr=" +
                            str(ranker))
      for axie in getRecentTeam(ranker):
          axie_part = ''
          axie_stat = ''
          for stat in axie['statsParts']:
              if ('name' in stat):
                  axie_part += stat['name'] + ' | '
              if ('card' in stat):
                  axie_part += stat['card']
                  axie_part = axie_part + '\n'
              if ('stat' in stat):
                  axie_stat += stat['stat'].upper() + ':'
              if ('value' in stat):
                  axie_stat += str(stat['value']) + ', '
          axie_stat = axie_stat[0:-2]
          axie_part += '\n' + axie_stat
          embed.add_field(name=axie['class'],
                          value=axie_part,
                          inline=True)
      rank += 1
      await message.channel.send(embed=embed)
      # print(getRecentTeam(ranker))
      # await message.channel.send(getRecentTeam(ranker))
      # print(getAxieImage(ranker['']))