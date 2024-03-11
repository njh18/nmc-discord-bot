import os
import discord
import json
import aiocron
import requests
import asyncio
from replit import db
from API.getFloorAxiePrice import getFloorAxiePrice
from API.getAxieDetail import getAxieDetail
from API.getAxiePrice import getAxiePrice
from API.getAxieImage import getAxieImage
from API.getPriceTrend import getPriceTrend
from API.getTokenPrice import getSLPPrice, getAXSPrice, getETHPrice, getSgdPrice, getUsdPrice, getPhpPrice
from urlBuilder import urlBuilder
from API.getDailySLP import getDailySLP
from API.getClanSLP import getClanSLP
from roninAddConverter import roninAddConverter
from API.getGuildRonin import getGuildOwnRonin, getGuildMentionRonin, getGuildOwnScholarRonin, getGuildMentionScholarRonin
from API.getAxieStatsParts import getAxieStatsParts
from API.getLeaderboard import getLeaderboard
from API.getRecentTeam import getRecentTeam
from API.getMMR import getMMR
from API.getGuildAverageSLP import getGuildAverageSLP
# Import Functions from Core
from Core.forceAP import forceAP
# from sheets import loadDb
import pandas as pd
import pprint
from discord.ext import commands
from discord.utils import get
from forex_python.converter import CurrencyRates
from pycoingecko import CoinGeckoAPI

client = discord.Client()
bot_token = os.environ['TOKEN']

# LOADS GOOGLE SHEET
pp = pprint.PrettyPrinter()
# df = loadDb()
# pp.pprint(df)

# to use pprint
test = json.load((open("Database-filters.json")))
pp.pprint(test)

# # initialise database (Only need to do it once if you change the file)
# roninDb = json.load(open("Database-ronin.json"))
# filtersDb = json.load(open("Database-filters.json"))
# db.set_bulk({"roninAdd":roninDb["roninAdd"],"filters":filtersDb["filters"]})


## Bot-testing channel ID
## use https://crontab.guru/ to
@aiocron.crontab('*/30 * * * *')
async def cronjob1():
    eth_logo = 0
    axs_logo = 0
    slp_logo = 0
    for x in client.emojis:
        if x.id == 906217466781397022:
            eth_logo = x
    print("Running cronjob1")
    channel = client.get_channel(902556837445009448)
    embed = discord.Embed(title="Axie Prices",
                          description="Average axie prices in ETH and US$",
                          color=discord.Color.random())
    embed.set_thumbnail(
        url=
        "https://s.alicdn.com/@sc04/kf/H6ff5bea9b74745a790b7c41afdd61cdbl.png")
    for key in db["filters"]:
        name, url, eth_cost, usd_cost = getAxiePrice(key)
        msg = "{eth_logo} ETH {eth:.3f} | ".format(eth_logo=eth_logo,
            eth=eth_cost) + "🇺🇸US$ {usd:.0f} ".format(
                usd=usd_cost) + "\n [Link to the marketplace]({url})".format(
                    url=url)
        embed.add_field(name=name, value=msg, inline=False)
        getPriceTrend(key)
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

    # boolean to check for role of author (the person who sent message)

    # admin = False
    # developer = False
    # nmcmanager = False
    # moderator = False
    # nmcscholar = False

    # if "developer" in [y.name.lower() for y in message.author.roles]:
    #     developer = True
    # if "nmc manager" in [y.name.lower() for y in message.author.roles]:
    #     nmcmanager = True
    # if "moderator" in [y.name.lower() for y in message.author.roles]:
    #     moderator = True
    # if "nmc scholar" in [y.name.lower() for y in message.author.roles]:
    #     nmcscholar = True
    # if (message.author.top_role.permissions.administrator):
    #     admin = True
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
    
    eth_logo = list(filter(lambda x : x.id == 906217466781397022, client.emojis))[0]
    axs_logo = list(filter(lambda x : x.id == 906989187620798505, client.emojis))[0]
    slp_logo = list(filter(lambda x : x.id == 902080377710059530, client.emojis))[0]

    # Get the floor-axie prices
    if msg.startswith('$floor-axies'):
        quote = getFloorAxiePrice()
        await message.channel.send(quote)

    elif msg.startswith('$forceAP'):
      embed = forceAP(eth_logo)
        # embed = discord.Embed(title="Axie Prices",
        #                       description="Average axie prices in ETH and US$",
        #                       color=discord.Color.random())
        # embed.set_thumbnail(
        #     url=
        #     "https://s.alicdn.com/@sc04/kf/H6ff5bea9b74745a790b7c41afdd61cdbl.png"
        # )
        # for key in db["filters"]:
        #     name, url, eth_cost, usd_cost = getAxiePrice(key)
        #     msg = str(eth_logo) + "ETH {eth:.3f} | ".format(
        #         eth=eth_cost) + "🇺🇸US$ {usd:.0f} ".format(
        #             usd=usd_cost
        #         ) + "\n [Link to the marketplace]({url})".format(url=url)
        #     embed.add_field(name=name, value=msg, inline=False)
      await message.channel.send(embed=embed)

    elif msg.startswith('$dbupdate'):
        if (admin or nmcmanager or developer):
            roninDb = json.load(open("Database-ronin.json"))
            filtersDb = json.load(open("Database-filters.json"))
            db.set_bulk({
                "roninAdd": roninDb["roninAdd"],
                "filters": filtersDb["filters"]
            })
            print('database updated')
            await message.channel.send('Guild Database Updated')

    elif msg.startswith('$test'):
        # for key in db["prices"]:
        # 	getPriceTrend(key)
        # e = discord.Embed(title="Test", colour=discord.Colour(0x278d89))
        # e.set_image(f"images/pricegraphs/price-anemone.png")
        #await message.channel.send(embed = value)
        await message.channel.send("Testing")

    # Maybe can remove
    elif msg.startswith("$getAxieSearchUrl"):
        try:
            theString = msg.split("$getAxieSearchUrl ", 1)[1]
            axieList = theString.split(",")
            sentMsg = ""
            for axieId in axieList:
                sentMsg = sentMsg + urlBuilder(axieId) + "\n"
            await message.channel.send(sentMsg)
        except IndexError:
            await message.channel.send("No Input given!")

#maybe can remove
    elif msg.startswith("$buildprice"):
        buildName = msg.split("$buildprice ", 1)[1]
        msg = getAxiePrice(json.loads(db.get_raw("filters"))[buildName])[0]
        await message.channel.send(embed=msg)

    elif msg.startswith('$hashira'):
        if (admin):
            await message.channel.send(
                'https://tenor.com/view/tomioka-hashira-gurenge-kimetsu-no-gif-18003742'
            )
        else:
            await message.channel.send(
                'You are not a Hashira. Try again in 10,000 years.')

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
#Get SLP market price
    elif msg.startswith("$priceslp"):
        sgd_price, usd_price, php_price, eth_price, axs_price, week_high, week_low = getSLPPrice(
        )
        embed = discord.Embed(
            title="Smooth Love Potion ($SLP)", color=0xfe93a1
        ).set_thumbnail(
            url=
            'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
        )
        embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} | 🇸🇬 SGD$ {sgd:.3f} \n {eth_logo} ETH {eth:.8f} | {axs_logo} AXS {axs:.06f} \n".format(
            usd=usd_price,
            php=php_price,
            sgd=sgd_price,
            eth=eth_price,
            axs=axs_price,
            eth_logo=eth_logo,
            axs_logo=axs_logo)
        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$priceslp":
            amt = int(msg.split("$priceslp ", 1)[1])
            amt_str = str(amt) + "SLP {slp_logo}".format(slp_logo=slp_logo)
            usd_amt = usd_price * amt
            php_amt = php_price * amt
            sgd_amt = sgd_price * amt
            axs_amt = axs_price * amt
            eth_amt = eth_price * amt
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.1f} \n ↳ {axs_logo} AXS {axs_amt:.6f} | {eth_logo} ETH {eth_amt:.8f}".format(
                sgd_amt=sgd_amt,
                usd_amt=usd_amt,
                php_amt=php_amt,
                axs_logo=axs_logo,
                axs_amt=axs_amt,
                eth_logo=eth_logo,
                eth_amt=eth_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)
        else:
            embed.add_field(name="7-Day Price Range",
                            value="🇺🇸 USD$ {w_low:.2f}-{w_hi:.2f}".format(
                                usd=usd_price,
                                php=php_price,
                                w_hi=week_high,
                                w_low=week_low))
        await message.channel.send(embed=embed)

        # await message.channel.send(file=discord.File('images/slp_50.png'))
        # await message.channel.send(output_msg)
        # await message.channel.send(output_msg2)

    elif msg.startswith("$pricesgd"):
        usd_price, php_price, eth_price, axs_price, slp_price = getSgdPrice()

        embed = discord.Embed(
            title="Singapore Dollars ($SGD)", color=0x766572).set_thumbnail(
                url='https://i.ibb.co/8dZtBbM/Mask-Group-2.png')
        # not sure why custom emoji not updating
        embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} \n ETH {eth:.6f} | {axs_logo} AXS {axs:.4f} | {slp_logo} SLP {slp:.2f}".format(
            usd=usd_price,
            php=php_price,
            eth=eth_price,
            axs=axs_price,
            slp=slp_price,
            eth_logo=eth_logo,
            axs_logo=axs_logo,
            slp_logo=slp_logo)
        # embed_msg = "USD$ {usd:.3f} | PHP$ {php:.2f} | SLP {slp:.4f} \n ETH {eth:.8f} | AXS {axs:.4f}".format(usd = usd_price, php = php_price,eth=eth_price,slp=slp_price,axs=axs_price)
        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$pricesgd":
            amt = float(msg.split("$pricesgd ", 1)[1])
            amt_str = str(amt) + " SGD"
            usd_amt = usd_price * amt
            php_amt = php_price * amt
            axs_amt = axs_price * amt
            eth_amt = eth_price * amt
            slp_amt = slp_price * amt
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇵🇭 PHP {php_amt:,.0f} \n ↳ {eth_logo} ETH {eth_amt:,.4f} | {axs_logo} AXS {axs_amt:.4f} | {slp_logo} SLP {slp_amt:.2f}".format(
                usd_amt=usd_amt,
                php_amt=php_amt,
                eth_amt=eth_amt,
                eth_logo=eth_logo,
                axs_logo=axs_logo,
                axs_amt=axs_amt,
                slp_logo=slp_logo,
                slp_amt=slp_amt)
            # embed_msg2 = " ↳ USD$ {usd_amt:,.2f} | PHP {php_amt:,.0f} | SLP {slp_amt:.0f}\n ↳ ETH$ {eth_amt:.5f} | AXS {axs_amt:.3f}".format(usd_amt = usd_amt, php_amt = php_amt,slp_amt=slp_amt,eth_amt=eth_amt,axs_amt=axs_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)
        # else:
        # 	embed.add_field(name="7-Day Price Range", value="🇺🇸US$ {w_low:.2f}-{w_hi:.2f}".format(usd = usd_price, php = php_price, w_hi=week_high , w_low =week_low))
        await message.channel.send(embed=embed)  #Get AXS market price

    elif msg.startswith("$priceusd"):
        sgd_price, php_price, eth_price, axs_price, slp_price = getUsdPrice()
        embed = discord.Embed(
            title="United States Dollars ($USD)",
            color=0x766572).set_thumbnail(
                url='https://i.ibb.co/jksSvyY/Mask-Group-3.png')
        embed_msg = "🇸🇬 SGD$ {sgd:.2f} | 🇵🇭 PHP$ {php:.0f} \n {eth_logo} ETH {eth:.6f} | {axs_logo} AXS {axs:.4f} | {slp_logo} SLP {slp:.2f}".format(
            sgd=sgd_price,
            php=php_price,
            eth=eth_price,
            axs=axs_price,
            slp=slp_price,
            eth_logo=eth_logo,
            axs_logo=axs_logo,
            slp_logo=slp_logo)
        # embed_msg = "SGD$ {sgd:.2f} | PHP$ {php:.0f} | SLP {slp:.4f} \n ETH {eth:.8f} | AXS {axs:.4f}".format(sgd = sgd_price, php = php_price,eth=eth_price,slp=slp_price,axs=axs_price)
        # embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} \n".format(usd = usd_price, php = php_price) + str(eth_logo) + " ETH {eth:.6f} | ".format(eth = eth_price) + str(axs_logo) + " AXS {axs:.4f} | ".format(axs = axs_price) + str(slp_logo) + " SLP {slp:.2f} | ".format(slp = slp_price)

        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$priceusd":
            amt = int(msg.split("$priceusd ", 1)[1])
            amt_str = str(amt) + " USD"
            sgd_amt = sgd_price * amt
            php_amt = php_price * amt
            axs_amt = axs_price * amt
            eth_amt = eth_price * amt
            slp_amt = slp_price * amt
            embed_msg2 = " ↳ 🇸🇬 SGD$ {sgd_amt:,.2f} | 🇵🇭 PHP {php_amt:,.0f} \n ↳ {eth_logo} ETH {eth_amt:,.4f} | {axs_logo} AXS {axs_amt:.4f} | {slp_logo} SLP {slp_amt:.2f}".format(
                sgd_amt=sgd_amt,
                php_amt=php_amt,
                eth_amt=eth_amt,
                eth_logo=eth_logo,
                axs_logo=axs_logo,
                axs_amt=axs_amt,
                slp_logo=slp_logo,
                slp_amt=slp_amt)
            # embed_msg2 = " ↳ SGD$ {sgd_amt:,.2f} | PHP {php_amt:,.0f} | SLP {slp_amt:.0f}\n ↳ ETH$ {eth_amt:.5f} | AXS {axs_amt:.3f}".format(sgd_amt = usd_amt, php_amt = php_amt,slp_amt=slp_amt,eth_amt=eth_amt,axs_amt=axs_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)

        await message.channel.send(embed=embed)  #Get AXS market price

    elif msg.startswith("$pricephp"):
        usd_price, sgd_price, eth_price, axs_price, slp_price = getPhpPrice()

        embed = discord.Embed(
            title="Phillipines Pesos ($PHP)", color=0x766572).set_thumbnail(
                url="https://i.ibb.co/ThcC6TM/Mask-Group-4.png")
        embed_msg = "🇺🇸 USD$ {usd:.2f} | 🇸🇬 SGD$ {sgd:.2f} \n {eth_logo} ETH {eth:.6f} | {axs_logo} AXS {axs:.4f} | {slp_logo} SLP {slp:.2f}".format(
            sgd=sgd_price,
            usd=usd_price,
            eth=eth_price,
            axs=axs_price,
            slp=slp_price,
            eth_logo=eth_logo,
            axs_logo=axs_logo,
            slp_logo=slp_logo)
        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$pricephp":
            amt = int(msg.split("$pricephp ", 1)[1])
            amt_str = str(amt) + " PHP"
            usd_amt = usd_price * amt
            sgd_amt = sgd_price * amt
            axs_amt = axs_price * amt
            eth_amt = eth_price * amt
            slp_amt = slp_price * amt
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} \n ↳ {eth_logo} ETH {eth_amt:,.4f} | {axs_logo} AXS {axs_amt:.4f} | {slp_logo} SLP {slp_amt:.2f}".format(
                sgd_amt=sgd_amt,
                usd_amt=usd_amt,
                eth_amt=eth_amt,
                eth_logo=eth_logo,
                axs_logo=axs_logo,
                axs_amt=axs_amt,
                slp_logo=slp_logo,
                slp_amt=slp_amt)
            # embed_msg2 = " ↳ USD$ {usd_amt:,.2f} | SGD {sgd_amt:,.0f} | SLP {slp_amt:.0f}\n ↳ ETH$ {eth_amt:.5f} | AXS {axs_amt:.3f}".format(usd_amt = usd_amt, sgd_amt = sgd_amt,slp_amt=slp_amt,eth_amt=eth_amt,axs_amt=axs_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)
        await message.channel.send(embed=embed)  #Get AXS market price

    elif msg.startswith("$priceaxs"):
        sgd_price, usd_price, php_price, eth_price, slp_price, week_high, week_low = getAXSPrice(
        )
        embed = discord.Embed(
            title="Axie Infinity Coin ($AXS)", color=0x01befe
        ).set_thumbnail(
            url=
            'https://seeklogo.com/images/A/axie-infinity-axs-logo-57FE26A5DC-seeklogo.com.png'
        )
        embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} | 🇸🇬 SGD$ {sgd:.3f} \n {eth_logo} ETH {eth:.8f} | {slp_logo} SLP {slp:.0f} \n".format(
            usd=usd_price,
            php=php_price,
            sgd=sgd_price,
            eth=eth_price,
            slp=slp_price,
            eth_logo=eth_logo,
            slp_logo=slp_logo)
        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$priceaxs":
            amt = float(msg.split("$priceaxs ", 1)[1])
            amt_str = str(amt) + " AXS {axs_logo}".format(axs_logo=axs_logo)
            usd_amt = usd_price * amt
            php_amt = php_price * amt
            sgd_amt = sgd_price * amt
            slp_amt = slp_price * amt
            eth_amt = eth_price * amt
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.0f}\n ↳ 🇸🇬 SGD$ {sgd:.3f} | ".format(
                usd_amt=usd_amt, php_amt=php_amt,
                sgd=sgd_amt) + str(eth_logo) + "ETH {eth_amt:,.4f}".format(
                    eth_amt=eth_amt)
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.1f} \n ↳ {slp_logo} SLP {slp_amt:.0f} | {eth_logo} ETH {eth_amt:.4f}".format(
                sgd_amt=sgd_amt,
                usd_amt=usd_amt,
                php_amt=php_amt,
                slp_logo=slp_logo,
                slp_amt=slp_amt,
                eth_logo=eth_logo,
                eth_amt=eth_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)
        else:
            embed.add_field(name="7-Day Price Range",
                            value="🇺🇸 USD$ {w_low:.2f}-{w_hi:.2f}".format(
                                usd=usd_price,
                                php=php_price,
                                w_hi=week_high,
                                w_low=week_low))
        # await message.channel.send(embed=embed)
        # await message.channel.send(file=discord.File('images/axs_50.png'))
        await message.channel.send(embed=embed)

    elif msg.startswith("$priceeth"):
        sgd_price, usd_price, php_price, slp_price, axs_price, week_high, week_low = getETHPrice(
        )
        embed = discord.Embed(
            title="Ethereum ($ETH)", color=0x627eea).set_thumbnail(
                url='https://i.ibb.co/y5NBSd2/eth-logo-1.png')
        embed_msg = "🇺🇸 USD$ {usd:.0f} | 🇵🇭 PHP$ {php:.0f} | 🇸🇬 SGD$ {sgd:.0f} \n {slp_logo} SLP {slp:.0f} | {axs_logo} AXS {axs:.0f} \n".format(
            usd=usd_price,
            php=php_price,
            sgd=sgd_price,
            slp=slp_price,
            axs=axs_price,
            slp_logo=slp_logo,
            axs_logo=axs_logo)
        embed.add_field(name='Current Price', value=embed_msg, inline=False)
        embed.set_footer(text='💂 Hail Nephy.')
        if msg != "$priceeth":
            amt = float(msg.split("$priceeth ", 1)[1])
            amt_str = str(amt) + " ETH {eth_logo}".format(eth_logo=eth_logo)
            usd_amt = usd_price * amt
            php_amt = php_price * amt
            sgd_amt = sgd_price * amt
            axs_amt = axs_price * amt
            slp_amt = slp_price * amt
            embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.0f} | 🇸🇬 SGD {sgd_amt:,.0f} | 🇵🇭 PHP$ {php_amt:,.0f} \n ↳ {axs_logo} AXS {axs_amt:.2f} | {slp_logo} SLP {slp_amt:.0f}".format(
                sgd_amt=sgd_amt,
                usd_amt=usd_amt,
                php_amt=php_amt,
                axs_logo=axs_logo,
                axs_amt=axs_amt,
                slp_logo=slp_logo,
                slp_amt=slp_amt)
            embed.add_field(name=amt_str, value=embed_msg2, inline=False)
        else:
            embed.add_field(name="7-Day Price Range",
                            value="🇺🇸 USD$ {w_low:.2f}-{w_hi:.2f}".format(
                                usd=usd_price, w_hi=week_high, w_low=week_low))
        # await message.channel.send(embed=embed)
        # await message.channel.send(file=discord.File('images/axs_50.png'))
        await message.channel.send(embed=embed)

#Get SLP from current
    elif msg.startswith("$roninslp"):
        roninAdd = msg.split("$slp ", 1)[1]
        await message.channel.send(embed=getDailySLP(roninAdd))

    elif msg.startswith("$myslp"):
        ronin = 0
        # if self
        if (len(msg.split(" ", 1)) == 1):
          if(nmcscholar):
            ronin = getGuildOwnScholarRonin(message.author.id)
          else:
            ronin = getGuildOwnRonin(message.author.id)
          if (ronin == None):
             await message.channel.send("User not found in NMC database!")
          else:
            await message.channel.send(
                    "Let me make a quick trip down to Lunacia to retrieve that information!"
                )
            await message.channel.send(embed=getDailySLP(ronin))

# if added a mention
        else:
            # if admin, get ronin of mentioned
            if (admin or nmcmanager or developer or moderator or message.author.id == 772847165550755900):
              mention = msg.split(" ", 1)[1]
              if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
                ronin=getGuildMentionScholarRonin(message.mentions[0].id)
              else:
                ronin = getGuildMentionRonin(mention)
              if (ronin == 0):
                await message.channel.send("User not found in NMC database!")
              else:
                await message.channel.send("Let me make a quick trip down to Lunacia to retrieve that information!")
                await message.channel.send(embed=getDailySLP(ronin))
            else:
                await message.channel.send("Mind your own business.")


    elif msg.startswith("$roninmmr"):
        await message.channel.send("Hold on, let me ask ma boy Neph.")
        ronin = msg.split(" ", 1)[1]
        await message.channel.send(embed=getMMR(ronin))

    elif msg.startswith("$mymmr"):
      ronin = 0
        # if self
      if (len(msg.split(" ", 1)) == 1):
        if(nmcscholar):
          ronin = getGuildOwnScholarRonin(message.author.id)
        else:
          ronin = getGuildOwnRonin(message.author.id)
        if (ronin == None):
          await message.channel.send("User not found in NMC database!")
        else:
          await message.channel.send("Hold on, let me ask ma boy Neph.")
          await message.channel.send(embed=getMMR(ronin))

# if added a mention
      else:
        if (admin or nmcmanager or developer or moderator or message.author.id == 772847165550755900):
          mention = msg.split(" ", 1)[1]
          if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
            ronin=getGuildMentionScholarRonin(message.mentions[0].id)
          else:
            ronin = getGuildMentionRonin(mention)
          if (ronin == 0):
            await message.channel.send("User not found in NMC database!")
          else:
            await message.channel.send("Hold on, let me ask ma boy Neph.")
            await message.channel.send(embed=getMMR(ronin))
        else:
          await message.channel.send("Mind your own business.")

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

    elif msg.startswith("$melhyu"):
        await message.channel.send(embed=discord.Embed(
            title=" Love of Nephy's life ❤️", color=0xf60ea1))

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

    elif msg.startswith("$myronin"):
        ronin = 0
        # if self
        if (len(msg.split(" ", 1)) == 1):
            ronin = getGuildOwnRonin(message.author.id)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                await message.channel.send(ronin)

# if added a mention
        else:
            mention = msg.split(" ", 1)[1]
            ronin = getGuildMentionRonin(mention)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                await message.channel.send(ronin)

    elif msg.startswith("$myscholarronin"):
        ronin = 0
        # if self
        if (len(msg.split(" ", 1)) == 1):
            ronin = getGuildOwnScholarRonin(message.author.id)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                await message.channel.send(ronin)

# if added a mention
        else:
            mention = msg.split(" ", 1)[1]
            ronin = getGuildMentionScholarRonin(mention)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                await message.channel.send(ronin)

    elif msg.startswith("$myaxielink"):
        ronin = 0
        # if self
        if (len(msg.split(" ", 1)) == 1):
          if(nmcscholar):
            ronin = getGuildOwnScholarRonin(message.author.id)
          else:
            ronin = getGuildOwnRonin(message.author.id)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                # await message.channel.send(ronin)
                return await message.channel.send(
                    'https://marketplace.axieinfinity.com/profile/' + ronin +
                    '/axie/')

# if added a mention
        else:
            mention = msg.split(" ", 1)[1]
            ronin = getGuildMentionRonin(mention)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
            else:
                return await message.channel.send(
                    'https://marketplace.axieinfinity.com/profile/' + ronin +
                    '/axie/')

    elif msg.startswith("$myaxie"):
        ronin = 0
# if self
        if (len(msg.split(" ", 1)) == 1):
          if(nmcscholar):
            ronin = getGuildOwnScholarRonin(message.author.id)
          else:
            ronin = getGuildOwnRonin(message.author.id)
            if (ronin == None):
                await message.channel.send("User not found in NMC database!")
                return      

# if added a mention
        else:
            # mentionedMember = msg.split(" ", 1)[1]
            if(len(list(filter(lambda x : x.name.lower() == "nmc scholar", message.mentions[0].roles)))>0):
              ronin=getGuildMentionScholarRonin(message.mentions[0].id)
            if (ronin == 0):
                await message.channel.send("User not found in NMC database")
                return
                
# first level check for noob axie message
        ronin = roninAddConverter(ronin)
        axies = getAxieDetail(ronin)
        for axie in axies:
          axieId = axie['id']
          axieClass = axie['class']
          axieImage = axie['image']
          embed = getAxieImage(axieId, axieClass, axieImage)
          await message.channel.send(embed = embed)

                
    elif msg.startswith("$archivedmyaxie"):
        ronin = 0
        # if self
        if (len(msg.split(" ", 1)) == 1):
            ronin = getGuildOwnRonin(message.author.id)
            if (ronin == None):
                await message.channel.send("Who tf are you?")
                return

# if added a mention
        else:
            mention = msg.split(" ", 1)[1]
            ronin = getGuildMentionRonin(mention)
            print(ronin)
            if (ronin == None):
                await message.channel.send("User not found in NMC database")
                return

# first level check for noob axie message
        ronin = roninAddConverter(ronin)
        response = requests.request(
            "GET",
            "https://game-api.axie.technology/battlelog/" + str(ronin),
            headers={},
            data={})
        json_data = json.loads(response.text)
        if (ronin != None and json_data[0] != {}):
            await message.channel.send('Here are your noob axies.')

        recent_team = getRecentTeam(ronin)
        if ((recent_team) == None):
            error_embed = discord.Embed(title="Axies not found 😢")
            error_embed.add_field(
                name="Network Error",
                value=
                "There seems to be problem with Axie's server at the moment. Please check back in abit."
            )
            await message.channel.send(embed=error_embed)

        for axie in recent_team:
            await message.channel.send(
                embed=getAxieImage(axie['id'], axie['class']))
        # await message.channel.send(getRecentTeam(ronin))

        # await message.channel.send(embed = getRecentTeam(ronin, message))


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

    elif msg.startswith('$swapslp'):
        sgd_price, usd_price, php_price, eth_price, week_high, week_low = getSLPPrice(
        )
        currency_logos = ['🇸🇬', '🇺🇸', '🇵🇭', eth_logo, slp_logo, axs_logo]
        currency_names = ['SGD', 'USD', 'PHP', 'ETH']

        # Choose currency
        embed = discord.Embed(title="Select Currency for Conversion")
        initial_message = await message.channel.send(embed=embed)
        for logo in currency_logos:
            await initial_message.add_reaction(logo)

        max_timer = 30
        check_timer = 0

        currency_logo = 0
        currency = 0

        while (check_timer < max_timer):
            print('waiting for input')
            await asyncio.sleep(5)
            initial_fetch = await message.channel.fetch_message(
                initial_message.id)
            print('waiting for input')
            for reaction in initial_fetch.reactions:
                print(reaction.count)
                if (reaction.count == 2):
                    currency_logo = reaction.emoji
                    currency = currency_names[currency_logos.index(
                        currency_logo)]
                    await message.channel.send(embed=discord.Embed(
                        title=
                        "Keep Checking, you really think you can huat overnight?"
                    ))
                    check_timer = max_timer
                check_timer += 5
                print(check_timer)
        if (currency == 0):
            initial_message = await message.channel.send(
                'No input received. Please try to \'$swapslp\' again.')
            return

# For each currency (Will Edit to make it less repetitive later)
        if (currency == 'SGD'):
            embed = discord.Embed(
                title="Smooth Love Potion ($SLP)", color=0xfe93a1
            ).set_thumbnail(
                url=
                'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
            )
            embed_msg = "SGD$ {sgd:.3f}".format(sgd=sgd_price)
            embed.add_field(name='Current Price',
                            value=embed_msg,
                            inline=False)
            embed.set_footer(text='💂 Hail Nephy.')
            if msg != "$swapslp":
                amt = float(msg.split("$swapslp ", 1)[1])
                amt_str = str(amt) + " SLP"
                sgd_amt = sgd_price * amt
                embed_msg2 = " ↳ SGD$ {sgd_amt:,.2f}".format(amt=amt,
                                                             sgd_amt=sgd_amt)
                embed.add_field(name=amt_str, value=embed_msg2, inline=False)
            await message.channel.send(embed=embed)

        if (currency == 'USD'):
            embed = discord.Embed(
                title="Smooth Love Potion ($SLP)", color=0xfe93a1
            ).set_thumbnail(
                url=
                'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
            )
            embed_msg = "US$ {usd:.3f}".format(usd=usd_price)
            embed.add_field(name='Current Price',
                            value=embed_msg,
                            inline=False)
            embed.set_footer(text='💂 Hail Nephy.')
            if msg != "$swapslpr":
                amt = float(msg.split("$swapslp ", 1)[1])
                amt_str = str(amt) + " SLP"
                usd_amt = usd_price * amt
                embed_msg2 = " ↳ US$ {usd_amt:,.2f}".format(amt=amt,
                                                            usd_amt=usd_amt)
                embed.add_field(name=amt_str, value=embed_msg2, inline=False)
            await message.channel.send(embed=embed)

        if (currency == 'PHP'):
            embed = discord.Embed(
                title="Smooth Love Potion ($SLP)", color=0xfe93a1
            ).set_thumbnail(
                url=
                'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
            )
            embed_msg = "PHP {php:.2f}".format(php=php_price)
            embed.add_field(name='Current Price',
                            value=embed_msg,
                            inline=False)
            embed.set_footer(text='💂 Hail Nephy.')
            if msg != "$swapslr":
                amt = float(msg.split("$swapslp ", 1)[1])
                amt_str = str(amt) + " SLP"
                php_amt = php_price * amt
                embed_msg2 = " ↳ PHP {php_amt:,.2f}".format(amt=amt,
                                                            php_amt=php_amt)
                embed.add_field(name=amt_str, value=embed_msg2, inline=False)
            await message.channel.send(embed=embed)

        if (currency == 'ETH'):
            embed = discord.Embed(
                title="Smooth Love Potion ($SLP)", color=0xfe93a1
            ).set_thumbnail(
                url=
                'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
            )
            embed_msg = "ETH {eth:.8f}".format(eth=eth_price)
            embed.add_field(name='Current Price',
                            value=embed_msg,
                            inline=False)
            embed.set_footer(text='💂 Hail Nephy.')
            if msg != "$swapslp":
                amt = float(msg.split("$swapslp ", 1)[1])
                amt_str = str(amt) + " SLP"
                eth_amt = eth_price * amt
                embed_msg2 = " ↳ ETH {eth_amt:,.2f}".format(amt=amt,
                                                            eth_amt=eth_amt)
                embed.add_field(name=amt_str, value=embed_msg2, inline=False)
            await message.channel.send(embed=embed)

    elif msg.startswith('$onboard'):
        if (admin or nmcmanager or developer):
            if (len(msg.split(" ", 1)) == 1):
                await message.channel.send(
                    "Can mention him/her after \'$onboard\'?")
            else:
                mention = msg.split(" ", 1)[1].replace('@', '').replace(
                    '<', '').replace('>', '').replace('!', '')
                print(mention)

                clan_emojis = [
                    '\N{Palm Tree}', '\N{Last Quarter Moon with Face}',
                    '\N{Hot Beverage}', '\N{Glowing Star}'
                ]
                clan_names = [
                    'oasis',
                    'lunar',
                    'kopi',
                    'sol',
                ]

                # Check Clan

                embed = discord.Embed(title="This paikia what clan one?",
                                      color=0x66a1a5)
                message1 = await message.channel.send(embed=embed)
                for emoji in clan_emojis:
                    await message1.add_reaction(emoji)

                max_timer = 30
                check_timer = 0

                clan_emoji = 0
                clan = 0

                while (check_timer < max_timer):
                    print('waiting to react to clan')
                    await asyncio.sleep(5)
                    message1fetch = await message.channel.fetch_message(
                        message1.id)
                    print('waited to react to clan')
                    for reaction in message1fetch.reactions:
                        print(reaction.count)
                        if (reaction.count == 2):
                            clan_emoji = reaction.emoji
                            clan = clan_names[clan_emojis.index(clan_emoji)]
                            # await message.channel.send('New scholar is from ' + clan + ' clan.')
                            await message.channel.send('\n Input received : ' +
                                                       clan.capitalize() +
                                                       ' clan. \n')
                            check_timer = max_timer
                    check_timer += 5
                    print(check_timer)
                if (clan == 0):
                    message1 = await message.channel.send(
                        'No input received. Please try to \'$onboard\' again.')
                    return

# Check Clan End
# Check Ronin

                embed = discord.Embed(title="Can paste ronin pls",
                                      color=0x66a1a5)
                message2 = await message.channel.send(embed=embed)

                check_timer = 0
                ronin = 0
                while (check_timer < max_timer):
                    print('waiting for ronin input')
                    # await asyncio.sleep(5)
                    try:
                        msg2 = await client.wait_for('message', timeout=5)
                    except:
                        print('waited 5s for ronin input')
                        check_timer += 5
                        print(check_timer)
                        continue
                    print(msg2.content)
                    message2fetch = msg2.content
                    # message2fetch = await message.channel.fetch_message(message2)

                    if (message2fetch.startswith('ronin:')):
                        ronin = message2fetch
                        print(ronin)
                        break
                    elif (message2fetch.startswith('0x')):
                        ronin = roninAddConverter(message2fetch)
                        print(ronin)
                        break
                    else:
                        await message.channel.send(
                            'Eh wrong format. Paste again.')
                        check_timer = 0
                        print('timer reset')
                    print(check_timer)
                if (ronin == 0):
                    message1 = await message.channel.send(
                        'Eh you don\'t know how to talk is it? Sorry hor go try from beginning - \'$onboard\' again.'
                    )
                    return
                else:
                    print("clan : " + clan)
                    print("ronin : " + str(ronin))
                    new_scholar = {
                        "userId": int(mention),
                        "managerShare": 5,
                        "eth": "",
                        "name": str(message.mentions[0].name),
                        "scholarRonin": ronin,
                        "investorPercentage": "",
                        "investorRonin": ""
                    }

                confirm_emojis = [
                    '\N{White Heavy Check Mark}', '\N{Cross Mark}'
                ]

                embed = discord.Embed(
                    title="Kindly confirm the details of new scholar",
                    color=0x66a1a5).add_field(
                        name="Discord Name : ",
                        value=str(message.mentions[0].name),
                        inline=False).add_field(
                            name="Clan : ",
                            value=clan.capitalize(),
                            inline=False).add_field(
                                name="User ID : ",
                                value=str(mention),
                                inline=False).add_field(
                                    name="Ronin Address : ",
                                    value=ronin,
                                    inline=False)
                message3 = await message.channel.send(embed=embed)
                for emoji in confirm_emojis:
                    await message3.add_reaction(emoji)

                max_timer = 30
                check_timer = 0

                clan_emoji = 0
                scholarConfirmed = False

                while (check_timer < max_timer):
                    print('waiting to confirm')
                    await asyncio.sleep(5)
                    message3fetch = await message.channel.fetch_message(
                        message3.id)
                    print('waited to confirm')
                    for reaction in message3fetch.reactions:
                        if (reaction.count == 2):
                            if (reaction.emoji == '\N{White Heavy Check Mark}'
                                ):
                                # scholarConfirmed=True
                                with open("Database-ronin.json",
                                          "r") as jsonFile:
                                    dbRonin = json.load(jsonFile)
                                dbRonin["roninAdd"][clan].append(new_scholar)
                                with open("Database-ronin.json",
                                          "w") as jsonFile:
                                    json.dump(dbRonin, jsonFile)
                                await message.channel.send(embed=discord.Embed(
                                    title=
                                    "Success! Scholar has been onboarded to NMC Database.",
                                    color=0x1abb9c))
                                return
                            elif (reaction.emoji == '\N{Cross Mark}'):
                                await message.channel.send(embed=discord.Embed(
                                    title=
                                    "Scholar Onboarding Cancelled. Please try \'$onboard\' again.",
                                    color=0xec4543))
                                return
                            check_timer = max_timer
                    check_timer += 5
                    print(check_timer)
                if (clan == 0):
                    message1 = await message.channel.send(
                        'No input received. Please try to \'$onboard\' again.')
                    return

client.run(bot_token)
'''
	LEGACY CODE
'''
'''
	elif msg.startswith("$slp"):
		ronin_id = msg.split("$slp ",1)[1]
		client_id, slp_total = get_slp(ronin_id)
		await message.channel.send("For ronin id "+str(client_id)+", your total slp is "+str(slp_total)+"! Congrats!")
'''
'''
	elif msg.startswith('$search'):
		try:
			url = msg.split("$search ",1)[1]
			quote = getAxiePrice(criteriaBuilder(url))[0]
			await message.channel.send(quote)
		except IndexError:
			await message.channel.send("No Input given!")
'''
'''
  # switch msg:
  #   case msg.startswith('$floor-axies'): 	
  #     # quote = getFloorAxiePrice()
  #     # await message.channel.send(quote)
  #     return 'hello'
  #     break

'''
