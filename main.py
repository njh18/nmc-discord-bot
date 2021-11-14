import os
import discord
import json
import aiocron
import requests
import asyncio
from replit import db
from Builder.urlBuilder import urlBuilder
from Builder.roninAddConverter import roninAddConverter
# Import Functions from API
from API.getFloorAxiePrice import getFloorAxiePrice
from API.getAxieDetail import getAxieDetail
from API.getAxiePrice import getAxiePrice
from API.getAxieImage import getAxieImage
from API.getAxieSaleTotal import getAxieSaleTotal
from API.getPriceTrend import getPriceTrend
from API.getTokenPrice import getSLPPrice, getAXSPrice, getETHPrice, getSgdPrice, getUsdPrice, getPhpPrice
from API.getDailySLP import getDailySLP
from API.getClanSLP import getClanSLP
from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin
from API.getAxieStatsParts import getAxieStatsParts
from API.getLeaderboard import getLeaderboard
from API.getRecentTeam import getRecentTeam
from API.getMMR import getMMR
from API.getGuildAverageSLP import getGuildAverageSLP
from API.getRole import getRole
# Import Functions from Core
from Core.forceAP import forceAP
from Core.priceSLP import priceSLP
from Core.priceSGD import priceSGD
from Core.priceUSD import priceUSD
from Core.pricePHP import pricePHP
from Core.priceAXS import priceAXS
from Core.priceETH import priceETH
from Core.mySLP import mySLP
from Core.myMMR import myMMR
from Core.myAxieLink import myAxieLink
from Core.myAxie import myAxie
from Core.myRonin import myRonin
from Core.myScholarRonin import myScholarRonin
from Core.dbUpdate import dbUpdate
from Core.getAxieSearchUrl import getAxieSearchUrl
from Core.cronJobNumber1 import cronJobNumber1
from Core.cronJobNumber0 import cronJobNumber0
from Core.swapSLP import swapSLP
from Core.onboard import onboard
# from sheets import loadDb
import pandas as pd
import pprint
from discord.ext import commands
from discord.utils import get
from forex_python.converter import CurrencyRates
from pycoingecko import CoinGeckoAPI
import schedule
import time

client = discord.Client()
bot_token = os.environ['TOKEN']

# LOADS GOOGLE SHEET
pp = pprint.PrettyPrinter()
# df = loadDb()
# pp.pprint(df)

# to use pprint
test = json.load((open("Database-filters.json")))
# pp.pprint(test)

# # initialise database (Only need to do it once if you change the file)
# roninDb = json.load(open("Database-ronin.json"))
# filtersDb = json.load(open("Database-filters.json"))
# db.set_bulk({"roninAdd":roninDb["roninAdd"],"filters":filtersDb["filters"]})

@aiocron.crontab("* * * * *")
async def cronjob0():
		# cronJobNumber0()	
		return

## Bot-testing channel ID
## use https://crontab.guru/ to
@aiocron.crontab('*/30 * * * *')
async def cronjob1():
  channel, embed = cronJobNumber1(client)
  print("end of cronjob1")
  await channel.send(embed=embed)
# await channel.send('This message is sent every 10 minutes')


# “At 8PM in UTC / 4PM SGT”
CHANNEL_ID = 899694611541409835



@aiocron.crontab('00 20 * * *')
async def cronjob2():
    print("Running cronjob2")
    for clan in json.loads(db.get_raw("roninAdd")):
        if clan != "singapore":
            channel = client.get_channel(905898436883275816)
            await channel.send("Retrieving Clan Info!")
            await channel.send(embed=getClanSLP(clan))


# when bot is ready to be use
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# bot = commands.Bot(command_prefix='$')


# Main Function -> When someone sends a message
@client.event
async def on_message(message):  

    if message.author == client.user:
        return
    msg = message.content

    developer = lambda x : True if "developer" in [y.name.lower() for y in message.author.roles] else False
    developer = developer(message)
    nmcmanager = lambda x : True if "nmc manager" in [y.name.lower() for y in message.author.roles] else False
    nmcmanager = nmcmanager(message)
    moderator = lambda x : True if "moderator" in [y.name.lower() for y in message.author.roles] else False
    moderator = moderator(message)
    nmcscholar = lambda x : True if "nmc scholar" in [y.name.lower() for y in message.author.roles] else False
    nmcscholar = nmcscholar(message)
    admin = lambda x : True if message.author.top_role.permissions.administrator else False
    admin = admin(message)  

    roles = getRole(message)  
    
    eth_logo = list(filter(lambda x : x.id == 906217466781397022, client.emojis))[0]
    axs_logo = list(filter(lambda x : x.id == 906989187620798505, client.emojis))[0]
    slp_logo = list(filter(lambda x : x.id == 902080377710059530, client.emojis))[0]

    # Get the floor-axie prices
    if msg.startswith('$floor-axies'):
        quote = getFloorAxiePrice()
        await message.channel.send(quote)

    elif msg.startswith('$forceAP'):
      embed = forceAP(eth_logo)
      await message.channel.send(embed=embed)

    elif msg.startswith('$dbupdate'):
      dbUpdate(admin, nmcmanager, developer)
      await message.channel.send('Guild Database Updated')

    # Maybe can remove
    elif msg.startswith("$getAxieSearchUrl"):
      output = getAxieSearchUrl(message)
      await message.channel.send(output)

    # maybe can remove
    elif msg.startswith("$buildprice"):
        buildName = msg.split("$buildprice ", 1)[1]
        msg = getAxiePrice(json.loads(db.get_raw("filters"))[buildName])[0]
        await message.channel.send(embed=msg)

    # Get Currency Conversion price
    elif msg.startswith("$priceslp"):
      embed = priceSLP(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    elif msg.startswith("$pricesgd"):
      embed = priceSGD(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    elif msg.startswith("$priceusd"):
      embed = priceUSD(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    elif msg.startswith("$pricephp"):
      embed = pricePHP(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    elif msg.startswith("$priceaxs"):
      embed = priceAXS(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    elif msg.startswith("$priceeth"):
      embed = priceETH(eth_logo, axs_logo, slp_logo, msg)
      await message.channel.send(embed=embed)

    # Get SLP from current
    elif msg.startswith("$roninslp"):
        roninAdd = msg.split("$slp ", 1)[1]
        await message.channel.send(embed=getDailySLP(roninAdd))

    elif msg.startswith("$myslp"):
      output, ronin = mySLP(message, nmcscholar, admin, nmcmanager, developer, moderator)
      await message.channel.send(output)
      if (ronin != 0):
        await message.channel.send(embed = getDailySLP(ronin))

    elif msg.startswith("$roninmmr"):
        await message.channel.send("Hold on, let me ask ma boy Neph.")
        ronin = msg.split(" ", 1)[1]
        await message.channel.send(embed=getMMR(ronin))

    elif msg.startswith("$mymmr"):
      output, ronin = myMMR(message, nmcscholar, admin, nmcmanager, developer, moderator)
      await message.channel.send(output)
      if (ronin != 0):
        await message.channel.send(embed = getMMR(ronin))     

    #Get SLP for entire Clan
    elif msg.startswith("$clanslp"):
        if (not (admin == True or moderator == True or developer == True
                 or nmcmanager == True) == True):
            return
        clan = msg.split("$clanslp ", 1)[1]
        await message.channel.send("Yes sir I am a slave..")
        await message.channel.send(embed=getClanSLP(clan))
        # await message.channel.send('nah, 好了. ' + clan + ' Clan MMR & SLP info retrieved.')

    #Get SLP for entire Clan
    elif msg.startswith("$guildavgslp"):
        if (not (admin == True or moderator == True or developer == True
                 or nmcmanager == True) == True):
            return
        min_slp = msg.split("$guildavgslp ", 1)[1]
        await message.channel.send(
            "Please wait.. Fetching a list of scholars with less than " +
            min_slp + " average daily SLP..")
        embed_list = getGuildAverageSLP(min_slp)
        for embedz in embed_list:
            await message.channel.send(embed=embedz)

    elif msg.startswith("$myronin"):
      output = myRonin(message)
      await message.channel.send(output)

    elif msg.startswith("$myscholarronin"):
      output = myScholarRonin(message)
      await message.channel.send(output)

    elif msg.startswith("$myaxielink"):
      await message.channel.send(myAxieLink(message, nmcscholar, admin, nmcmanager, developer, moderator))

    elif msg.startswith("$myaxie"):
      output, axies = myAxie(message, nmcscholar)
      if (output != ""):
        await message.channel.send(output)
      for axie in axies[:3]:
          embed = getAxieImage(axie['id'], axie['class'], axie['image'])
          await message.channel.send(embed = embed)

    elif msg.startswith('$swapslp'):
      asyncio.get_event_loop().create_task(swapSLP(message, eth_logo, axs_logo))

    elif msg.startswith('$onboard'):
      asyncio.get_event_loop().create_task(onboard(message, admin, nmcmanager, developer))
#         if (admin or nmcmanager or developer):
#             if (len(msg.split(" ", 1)) == 1):
#                 await message.channel.send(
#                     "Can mention him/her after \'$onboard\'?")
#             else:
#                 mention = msg.split(" ", 1)[1].replace('@', '').replace(
#                     '<', '').replace('>', '').replace('!', '')
#                 print(mention)

#                 clan_emojis = [
#                     '\N{Palm Tree}', '\N{Last Quarter Moon with Face}',
#                     '\N{Hot Beverage}', '\N{Glowing Star}'
#                 ]
#                 clan_names = [
#                     'oasis',
#                     'lunar',
#                     'kopi',
#                     'sol',
#                 ]

#                 # Check Clan

#                 embed = discord.Embed(title="This paikia what clan one?",
#                                       color=0x66a1a5)
#                 message1 = await message.channel.send(embed=embed)
#                 for emoji in clan_emojis:
#                     await message1.add_reaction(emoji)

#                 max_timer = 30
#                 check_timer = 0

#                 clan_emoji = 0
#                 clan = 0

#                 while (check_timer < max_timer):
#                     print('waiting to react to clan')
#                     await asyncio.sleep(5)
#                     message1fetch = await message.channel.fetch_message(
#                         message1.id)
#                     print('waited to react to clan')
#                     for reaction in message1fetch.reactions:
#                         print(reaction.count)
#                         if (reaction.count == 2):
#                             clan_emoji = reaction.emoji
#                             clan = clan_names[clan_emojis.index(clan_emoji)]
#                             # await message.channel.send('New scholar is from ' + clan + ' clan.')
#                             await message.channel.send('\n Input received : ' +
#                                                        clan.capitalize() +
#                                                        ' clan. \n')
#                             check_timer = max_timer
#                     check_timer += 5
#                     print(check_timer)
#                 if (clan == 0):
#                     message1 = await message.channel.send(
#                         'No input received. Please try to \'$onboard\' again.')
#                     return

# # Check Clan End
# # Check Ronin

#                 embed = discord.Embed(title="Can paste ronin pls",
#                                       color=0x66a1a5)
#                 message2 = await message.channel.send(embed=embed)

#                 check_timer = 0
#                 ronin = 0
#                 while (check_timer < max_timer):
#                     print('waiting for ronin input')
#                     # await asyncio.sleep(5)
#                     try:
#                         msg2 = await client.wait_for('message', timeout=5)
#                     except:
#                         print('waited 5s for ronin input')
#                         check_timer += 5
#                         print(check_timer)
#                         continue
#                     print(msg2.content)
#                     message2fetch = msg2.content
#                     # message2fetch = await message.channel.fetch_message(message2)

#                     if (message2fetch.startswith('ronin:')):
#                         ronin = message2fetch
#                         print(ronin)
#                         break
#                     elif (message2fetch.startswith('0x')):
#                         ronin = roninAddConverter(message2fetch)
#                         print(ronin)
#                         break
#                     else:
#                         await message.channel.send(
#                             'Eh wrong format. Paste again.')
#                         check_timer = 0
#                         print('timer reset')
#                     print(check_timer)
#                 if (ronin == 0):
#                     message1 = await message.channel.send(
#                         'Eh you don\'t know how to talk is it? Sorry hor go try from beginning - \'$onboard\' again.'
#                     )
#                     return
#                 else:
#                     print("clan : " + clan)
#                     print("ronin : " + str(ronin))
#                     new_scholar = {
#                         "userId": int(mention),
#                         "managerShare": 5,
#                         "eth": "",
#                         "name": str(message.mentions[0].name),
#                         "scholarRonin": ronin,
#                         "investorPercentage": "",
#                         "investorRonin": ""
#                     }

#                 confirm_emojis = [
#                     '\N{White Heavy Check Mark}', '\N{Cross Mark}'
#                 ]

#                 embed = discord.Embed(
#                     title="Kindly confirm the details of new scholar",
#                     color=0x66a1a5).add_field(
#                         name="Discord Name : ",
#                         value=str(message.mentions[0].name),
#                         inline=False).add_field(
#                             name="Clan : ",
#                             value=clan.capitalize(),
#                             inline=False).add_field(
#                                 name="User ID : ",
#                                 value=str(mention),
#                                 inline=False).add_field(
#                                     name="Ronin Address : ",
#                                     value=ronin,
#                                     inline=False)
#                 message3 = await message.channel.send(embed=embed)
#                 for emoji in confirm_emojis:
#                     await message3.add_reaction(emoji)

#                 max_timer = 30
#                 check_timer = 0

#                 clan_emoji = 0
#                 scholarConfirmed = False

#                 while (check_timer < max_timer):
#                     print('waiting to confirm')
#                     await asyncio.sleep(5)
#                     message3fetch = await message.channel.fetch_message(
#                         message3.id)
#                     print('waited to confirm')
#                     for reaction in message3fetch.reactions:
#                         if (reaction.count == 2):
#                             if (reaction.emoji == '\N{White Heavy Check Mark}'
#                                 ):
#                                 # scholarConfirmed=True
#                                 with open("Database-ronin.json",
#                                           "r") as jsonFile:
#                                     dbRonin = json.load(jsonFile)
#                                 dbRonin["roninAdd"][clan].append(new_scholar)
#                                 with open("Database-ronin.json",
#                                           "w") as jsonFile:
#                                     json.dump(dbRonin, jsonFile)
#                                 await message.channel.send(embed=discord.Embed(
#                                     title=
#                                     "Success! Scholar has been onboarded to NMC Database.",
#                                     color=0x1abb9c))
#                                 return
#                             elif (reaction.emoji == '\N{Cross Mark}'):
#                                 await message.channel.send(embed=discord.Embed(
#                                     title=
#                                     "Scholar Onboarding Cancelled. Please try \'$onboard\' again.",
#                                     color=0xec4543))
#                                 return
#                             check_timer = max_timer
#                     check_timer += 5
#                     print(check_timer)
#                 if (clan == 0):
#                     message1 = await message.channel.send(
#                         'No input received. Please try to \'$onboard\' again.')
#                     return

    elif msg.startswith("$leaderboard"):
        offset = 1
        limit = 2
        print(len(msg.split(' ')))
        if (len(msg.split(' ')) > 1):
            params = msg.split("$leaderboard ", 1)[1]
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

    # Anime and Fun
    elif msg.startswith('$hashira'):
        if (admin):
            await message.channel.send(
                'https://tenor.com/view/tomioka-hashira-gurenge-kimetsu-no-gif-18003742'
            )
        else:
            await message.channel.send(
                'You are not a Hashira. Try again in 10,000 years.')

    elif msg.startswith("$melhyu"):
        await message.channel.send(embed=discord.Embed(
            title=" Love of Nephy's life ❤️", color=0xf60ea1))

    elif msg.startswith('$rengokusan'):
        if (admin):
            await message.channel.send(
                '  https://tenor.com/view/demon-slayer-movie-rengoku-sword-anime-gif-15690515'
            )
        else:
            await message.channel.send(
                'You are 10,000 years too early to be calling Rengoku-san')

    elif msg.startswith('$nezuko'):
        await message.channel.send('https://tenor.com/view/nezuko-gif-21668450'
                                   )

    elif msg.startswith('$chandra'):
        await message.channel.send(
            '☃️ iZ biGinNinGz tU LuK aL0rT Laik kUrisU masU ☃️')
        await message.channel.send(
            'https://tenor.com/view/merry-christmas-happy-holidays-baby-jesus-snow-gif-15888940'
        )

    # Testing Codes                
    elif msg.startswith('$test'):
      await message.channel.send("Eh mai test liao la")    
    
    elif msg.startswith('$asd'):

        roninAddDb = json.loads(db.get_raw("roninAdd"))
        print(type(roninAddDb))
        print(type(roninAddDb["Oasis"]))
        print(roninAddDb["Oasis"])

    elif msg.startswith('$dsa'):

      print(developer)
      print(nmcmanager)
      print(moderator)
      print(nmcscholar)
      print(admin)
      # admin = False
      # developer = False
      # nmcmanager = False
      # moderator = False
      # nmcscholar = False

      # if "developer" in [y.name.lower() for y in message.author.roles]:
      #   developer = True
      # if "nmc manager" in [y.name.lower() for y in message.author.roles]:
      #   nmcmanager = True
      # if "moderator" in [y.name.lower() for y in message.author.roles]:
      #   moderator = True
      # if "nmc scholar" in [y.name.lower() for y in message.author.roles]:
      #   nmcscholar = True
      # admin = message.author.top_role.permissions.administrator ? True : False
      #   admin = True
    
        
      # eth_logo = list(filter(lambda x : x.id == 906217466781397022, client.emojis))[0]
      # axs_logo = list(filter(lambda x : x.id == 906989187620798505, client.emojis))[0]
      # slp_logo = list(filter(lambda x : x.id == 902080377710059530, client.emojis))[0]
      
client.run(bot_token)