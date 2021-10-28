import os
import discord
import json
import aiocron
import requests
from replit import db
from getFloorAxiePrice import getFloorAxiePrice
from getAxiePrice import getAxiePrice
from getAxieImage import getAxieImage
from getPriceTrend import getPriceTrend
from getTokenPrice import getSLPPrice, getAXSPrice
from urlBuilder import urlBuilder
from getDailySLP import getDailySLP
from getClanSLP import getClanSLP
from roninAddConverter import roninAddConverter
from getGuildRonin import getGuildOwnRonin, getGuildMentionRonin
from getAxieStatsParts import getAxieStatsParts

client = discord.Client();
bot_token = os.environ['TOKEN']


# # initialise database (Only need to do it once if you change the file)
# roninDb = json.load(open("Database-ronin.json"))
# filtersDb = json.load(open("Database-filters.json"))
# db.set_bulk({"roninAdd":roninDb["roninAdd"],"filters":filtersDb["filters"]})

# for key in db["prices"]:
# 	print(key)
# 	for theList in db["prices"][key]:
# 		print(theList.value)


## Bot-testing channel ID
## use https://crontab.guru/ to 
@aiocron.crontab('*/30 * * * *')
async def cronjob1():
		print("Running cronjob1")
		channel = client.get_channel(902556837445009448)
		for key in db["filters"]:
				value = getAxiePrice(key)
				await channel.send(embed = value)
    # await channel.send('This message is sent every 10 minutes')

# will be used for ronin 
ADMIN_CHANNEL_ID = os.environ["ADMIN_CHANNEL_ID"]
# “At 00:00.”
## NOTE: CANNOT GO TO ADMIN, I THINK NEED ADMIN RIGHTS
CHANNEL_ID = 899694611541409835
@aiocron.crontab('00 16 * * *')
async def cornjob2():
		print("Running cronjob2")
		for clan in json.loads(db.get_raw("roninAdd")):
			channel = client.get_channel(CHANNEL_ID)
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
  
	admin = False
	if(message.author.top_role.permissions.administrator):
		admin = True
	msg = message.content

	# Get the floor-axie prices
	if msg.startswith('$floor-axies'):
		quote = getFloorAxiePrice()
		await message.channel.send(quote)


	elif msg.startswith('$test'):
		for key in db["prices"]:
			getPriceTrend(key)
		#await message.channel.send(embed = value)
		await message.channel.send("Testing now")

	# Maybe can remove
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
			msg = getAxiePrice(json.loads(db.get_raw("filters"))[buildName])[0]
			await message.channel.send(embed = msg)

	elif msg.startswith('$hashira'):
		if(admin):
			await message.channel.send('https://tenor.com/view/tomioka-hashira-gurenge-kimetsu-no-gif-18003742')
		else:
			await message.channel.send('You are not a Hashira. Try again in 10,000 years.')
	elif msg.startswith('$rengokusan'):
		if(admin):
			await message.channel.send('  https://tenor.com/view/demon-slayer-movie-rengoku-sword-anime-gif-15690515')
		else:
			await message.channel.send('You are 10,000 years too early to be calling Rengoku-san')

	elif msg.startswith('$nezuko'):
		await message.channel.send('https://tenor.com/view/nezuko-gif-21668450')

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

  #Get SLP from current 
	elif msg.startswith("$slp"):
		roninAdd = msg.split("$slp ",1)[1]
		await message.channel.send(embed=getDailySLP(roninAdd))

	elif msg.startswith("$myslp"):
		ronin=0
    
    # if self
		if(len(msg.split(" ",1))==1):
			
			ronin = getGuildOwnRonin(message.author.id)
			if(ronin==None):
				await message.channel.send("User not found in NMC database!")
			else:
				await message.channel.send("Let me make a quick trip down to Lunacia to retrieve that information!")
				await message.channel.send(embed = getDailySLP(ronin))

    # if added a mention
		else:
			print('2')
      # if admin, get ronin of mentioned
			if(admin):
				mention = msg.split(" ",1)[1]
				ronin = getGuildMentionRonin(mention)
				if(ronin==None):
					await message.channel.send("User not found in NMC database!")
				else:
					await message.channel.send("Let me make a quick trip down to Lunacia to retrieve   that information!")
					await message.channel.send(embed = getDailySLP(ronin))
			else:
				await message.channel.send("Mind your own business.")
  	#await message.channel.send(client.get_user(roninAdd))
  	# await message.channel.send(embed=getDailySLP(roninAdd))

	#Get SLP for entire Clan
	elif msg.startswith("$clanslp"):
		clan = msg.split("$clanslp ",1)[1]
		await message.channel.send(embed = getClanSLP(clan))

	elif msg.startswith("$melhyu"):
		await message.channel.send(embed = discord.Embed(title= " Love of Nephy's life ❤️", color=0xf60ea1))

	elif msg.startswith("$myronin"):
		ronin=0
    # if self
		if(len(msg.split(" ",1))==1):
			ronin = getGuildOwnRonin(message.author.id)
			if(ronin==None):
				await message.channel.send("User not found in NMC database!")
			else:
				await message.channel.send(ronin)

    # if added a mention
		else:
			mention = msg.split(" ",1)[1]
			ronin = getGuildMentionRonin(mention)
			if(ronin==None):
				await message.channel.send("User not found in NMC database!")
			else:
					await message.channel.send(ronin)

	elif msg.startswith("$myaxie"):
		ronin=0
    # if self
		if(len(msg.split(" ",1))==1):
			ronin = getGuildOwnRonin(message.author.id)
			if(ronin==None):
				await message.channel.send("Who tf are you?")
				return

    # if added a mention
		else:
			mention = msg.split(" ",1)[1]

			ronin = getGuildMentionRonin(mention)
			print(ronin)
			if(ronin==None):
				await message.channel.send("User not found in NMC database")
				return


		ronin=roninAddConverter(ronin)
    # if added a
		url = "https://game-api.axie.technology/battlelog/" + str(ronin)
		print(url)
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		json_data = json.loads(response.text)

		try:
			if(ronin!=None and json_data[0]!={}):
				await message.channel.send('Here are your noob axies.')
      	# print(json_data[0])

			client_id = ''
			if(str(ronin) == json_data[0]['items'][0]['first_client_id']):
				client_id=json_data[0]['items'][0]['first_team_id']
			else:
				client_id=json_data[0]['items'][0]['second_team_id']

			for fighter in json_data[0]['items'][0]['fighters']:
				if(fighter['team_id']==client_id):
					getAxieStatsParts(fighter['fighter_id'])
					# print(getAxieStatsParts(fighter['fighter_id']))
					await message.channel.send(embed = getAxieImage(fighter['fighter_id'],fighter['fighter_class']))
		except:
				embed = discord.Embed(title = "Axies not found 😢")
				embed.add_field(name = "Network Error", value = "There seems to be problem with Axie's server at the moment. Please check back in abit.")
				await message.channel.send(embed = embed)




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