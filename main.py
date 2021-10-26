import os
import discord
import json
import aiocron
from replit import db
from getFloorAxiePrice import getFloorAxiePrice
from getAxiePrice import getAxiePrice
from criteriaBuilder import criteriaBuilder
from getTokenPrice import getSLPPrice, getAXSPrice
from urlBuilder import urlBuilder
from getDailySLP import getDailySLP
from getClanSLP import getClanSLP

client = discord.Client();
bot_token = os.environ['TOKEN']


# # initialise database
roninDb = json.load(open("Database-ronin.json"))
filtersDb = json.load(open("Database-filters.json"))
db.set_bulk({"roninAdd":roninDb["roninAdd"],"filters":filtersDb["filters"]})


## Bot-testing channel ID
## use https://crontab.guru/ to 
CHANNEL_ID = 899694611541409835
@aiocron.crontab('*/10 * * * *')
async def cornjob1():
    channel = client.get_channel(CHANNEL_ID)
    # await channel.send('This message is sent every 10 minutes')

# will be used for ronin 
ADMIN_CHANNEL_ID = os.environ["ADMIN_CHANNEL_ID"]
# “At 00:00.”
## NOTE: CANNOT GO TO ADMIN, I THINK NEED ADMIN RIGHTS
@aiocron.crontab('20 16 * * *')
async def cornjob2():
		for clan in json.loads(db.get_raw("roninAdd")):
			channel = client.get_channel(899694611541409835)
			await channel.send(embed = getClanSLP(clan))


# when bot is ready to be use
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# Main Function -> When someone sends a message
@client.event
async def on_message(message):
	if message.author == client.user:
		return
  
	msg = message.content
  # switch msg:
  #   case msg.startswith('$floor-axies'): 	
  #     # quote = getFloorAxiePrice()
  #     # await message.channel.send(quote)
  #     return 'hello'
  #     break


	# Get the floor-axie prices
	if msg.startswith('$floor-axies'):
		quote = getFloorAxiePrice()
		await message.channel.send(quote)

	elif msg.startswith('$search'):
		try:
			url = msg.split("$search ",1)[1]
			quote = getAxiePrice(criteriaBuilder(url))
			await message.channel.send(quote)
		except IndexError:
			await message.channel.send("No Input given!")

	elif msg.startswith("$getAxieSearchUrl"):
		try:
			theString = msg.split("$getAxieSearchUrl ",1)[1]
			axieList = theString.split(",")
			sentMsg = ""
			for axieId in axieList:
				sentMsg = sentMsg + urlBuilder(axieId) + "\n"
			await message.channel.send(sentMsg)
		except IndexError:
			await message.channel.send("No Input given!")

	elif msg.startswith("$buildprice"):
			buildName = msg.split("$buildprice ",1)[1]
			msg = getAxiePrice(json.loads(db.get_raw("filters"))[buildName])
			await message.channel.send(msg)


	elif msg.startswith('$hashira'):
		if(message.author.top_role.permissions.administrator):
			await message.channel.send('https://tenor.com/view/demon-slayer-movie-rengoku-sword-anime-gif-15690515')
		else:
			await message.channel.send('You are not a Hashira. Try again in 10,000 years.')
  
	elif msg.startswith('$rengokusan'):
		await message.channel.send('diam la kopimuji is chandra doxxed')

  #Get SLP market price
	elif msg.startswith("$priceslp"):
		usd_price, php_price, week_high, week_low = getSLPPrice()
		output_msg = "Current Price: US$ {usd:.3f} | Php {php:.2f}\n7D Range: US$ {w_low:.3f}-{w_hi:.3f}".format(usd = usd_price, php = php_price, w_hi=week_high, w_low =week_low)
		if msg != "$priceslp":
			amt = int(msg.split("$priceslp ",1)[1])
			usd_amt = usd_price * amt
			php_amt = php_price * amt
			output_msg += "\n{amt} SLP = US$ {usd_amt:,.2f} | Php {php_amt:,.0f}".format(amt = amt, usd_amt = usd_amt, php_amt = php_amt)
			
		await message.channel.send(file=discord.File('images/slp_50.png'))
		await message.channel.send(output_msg)
  
 	#Get AXS market price
	elif msg.startswith("$priceaxs"):
		usd_price, php_price, week_high, week_low = getAXSPrice()
		output_msg = "Current Price: US$ {usd:,.2f} | Php {php:,.2f}\n7D Range: US$ {w_low:.2f}-{w_hi:.2f}".format(usd = usd_price, php = php_price, w_hi=week_high , w_low =week_low)
		if msg != "$priceaxs":
			amt = int(msg.split("$priceaxs ",1)[1])
			usd_amt = usd_price * amt
			php_amt = php_price * amt
			output_msg += "\n{amt} AXS = US$ {usd_amt:,.2f} | Php {php_amt:,.2f}".format(amt = amt, usd_amt = usd_amt, php_amt = php_amt)
		await message.channel.send(file=discord.File('images/axs_50.png'))
		await message.channel.send(output_msg)

  #Get SLP from 
	elif msg.startswith("$slp"):
		roninAdd = msg.split("$slp ",1)[1]
		await message.channel.send(embed=getDailySLP(roninAdd))


	# Test function
	elif msg.startswith("$test"):
		for clan in json.loads(db.get_raw("roninAdd")):
			await message.channel.send(embed = getClanSLP(clan))




	
'''
	elif msg.startswith("$slp"):
		ronin_id = msg.split("$slp ",1)[1]
		client_id, slp_total = get_slp(ronin_id)
		await message.channel.send("For ronin id "+str(client_id)+", your total slp is "+str(slp_total)+"! Congrats!")
'''

client.run(bot_token)

