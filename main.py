import os
import discord
from replit import db
from getFloorAxiePrice import getFloorAxiePrice
from getAxiePrice import getAxiePrice
from criteriaBuilder import criteriaBuilder
from getTokenPrice import getSLPPrice, getAXSPrice

client = discord.Client();
bot_token = os.environ['TOKEN']

# when bot is ready to be use
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return
  
	msg = message.content

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

	elif msg.startswith('$hashira'):
		await message.channel.send('https://tenor.com/view/demon-slayer-movie-rengoku-sword-anime-gif-15690515')
  
	elif msg.startswith('$rengokusan'):
		await message.channel.send('diam la nephy')

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
'''
	elif msg.startswith("$slp"):
		ronin_id = msg.split("$slp ",1)[1]
		client_id, slp_total = get_slp(ronin_id)
		await message.channel.send("For ronin id "+str(client_id)+", your total slp is "+str(slp_total)+"! Congrats!")
'''

client.run(bot_token)

