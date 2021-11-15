import os
import discord
import json
import aiocron
import asyncio
import math
from replit import db
# Import Functions from API
from API.getFloorAxiePrice import getFloorAxiePrice
from API.getAxiePrice import getAxiePrice
from API.getAxieImage import getAxieImage
from API.getDailySLP import getDailySLP
from API.getClanSLP import getClanSLP
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
from Core.swapSLP import swapSLP
from Core.onboard import onboard
from Core.offboard import offboard
from Core.leaderboard import leaderboard
# from sheets import loadDb
import pprint

client = discord.Client()
bot_token = os.environ['TOKEN']

# LOADS GOOGLE SHEET
pp = pprint.PrettyPrinter()

# # initialise database (Only need to do it once if you change the file)
# roninDb = json.load(open("Database-ronin.json"))
# filtersDb = json.load(open("Database-filters.json"))
# db.set_bulk({"roninAdd":roninDb["roninAdd"],"filters":filtersDb["filters"]})

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

    roles = getRole(message)  
    
    eth_logo = list(filter(lambda x : x.id == 906217466781397022, client.emojis))[0]
    axs_logo = list(filter(lambda x : x.id == 906989187620798505, client.emojis))[0]
    slp_logo = list(filter(lambda x : x.id == 902080377710059530, client.emojis))[0]

    # Get the floor-axie prices
    if msg.startswith('$floor-axies'):
        quote = getFloorAxiePrice()
        await message.channel.send(quote)

    elif msg.startswith('$morale'):
      # base = msg.split("$crit ", 1)[1]
      morale = msg.split("$morale ", 1)[1]
      dmg = math.sqrt(int(morale)) * 10 + int(morale) * 0.4 - 18
      await message.channel.send("crit damage : " + str(dmg))

    elif msg.startswith('$forceAP'):
      embed = forceAP(eth_logo)
      await message.channel.send(embed=embed)

    elif msg.startswith('$dbupdate'):
      dbUpdate(roles)
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
      output, ronin = mySLP(message, roles)
      await message.channel.send(output)
      if (ronin != 0):
        await message.channel.send(embed = getDailySLP(ronin))

    elif msg.startswith("$roninmmr"):
        await message.channel.send("Hold on, let me ask ma boy Neph.")
        ronin = msg.split(" ", 1)[1]
        await message.channel.send(embed=getMMR(ronin))

    elif msg.startswith("$mymmr"):
      output, ronin = myMMR(message, roles)
      await message.channel.send(output)
      if (ronin != 0):
        await message.channel.send(embed = getMMR(ronin))     

    #Get SLP for entire Clan
    elif msg.startswith("$clanslp"):
        permissions = ['admin', 'nmcmanager', 'developer', 'moderator']
        if (not any(role in permissions for role in roles)):
            return
        clan = msg.split("$clanslp ", 1)[1]
        await message.channel.send("Yes sir I am a slave..")
        await message.channel.send(embed=getClanSLP(clan))
        # await message.channel.send('nah, 好了. ' + clan + ' Clan MMR & SLP info retrieved.')

    #Get SLP for entire Clan
    elif msg.startswith("$guildavgslp"):
        permissions = ['admin', 'nmcmanager', 'developer', 'moderator']
        if (not any(role in permissions for role in roles)):
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
      await message.channel.send(myAxieLink(message, roles))

    elif msg.startswith("$myaxie"):
      output, axies = myAxie(message, roles)
      if (output != ""):
        await message.channel.send(output)
      for axie in axies[:3]:
          embed = getAxieImage(axie['id'], axie['class'], axie['image'])
          await message.channel.send(embed = embed)

    elif msg.startswith('$swapslp'):
      asyncio.get_event_loop().create_task(swapSLP(message, eth_logo, axs_logo))

    elif msg.startswith('$onboard'):
      asyncio.get_event_loop().create_task(onboard(message, roles, client))

    elif msg.startswith('$offboard'):
      asyncio.get_event_loop().create_task(offboard(message, roles))

    elif msg.startswith("$leaderboard"):
      asyncio.get_event_loop().create_task(leaderboard(message))

    # Anime and Fun
    elif msg.startswith('$hashira'):
        if ('admin' in roles):
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
        if ('admin' in roles):
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
      print(roles)
         
client.run(bot_token)