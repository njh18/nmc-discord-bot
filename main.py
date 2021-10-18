import os
import discord
from replit import db
from getFloorAxies import getFloorAxiePrice
from getAxiePrice import getAxiePrice
from criteriaBuilder import criteriaBuilder
from getTokenPrice import getSlpPrice, getAxsPrice

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

	if msg.startswith('$search'):
		try:
			url = msg.split("$search ",1)[1]
			quote = getAxiePrice(criteriaBuilder(url))
			await message.channel.send(quote)
		except IndexError:
			await message.channel.send("No Input given!")

  	if msg.startswith('$hashira'):
    	await message.channel.send('https://tenor.com/view/demon-slayer-movie-rengoku-sword-anime-gif-15690515')

  	#Get SLP market price
	if msg.startswith("$slpprice"):
		usd_price, php_price, week_high, week_low = getSlpPrice()
		output_msg = "Current Price: US$ {usd:.3f} | Php {php:.2f}\n7D Range: US$ {w_low:.3f}-{w_hi:.3f}".format(usd = usd_price, php = php_price, w_hi=week_high, w_low =week_low)
		if msg != "$slpprice":
			amt = int(msg.split("$slpprice ",1)[1])
			usd_amt = usd_price * amt
			php_amt = php_price * amt
			output_msg += "\n{amt} SLP = US$ {usd_amt:,.2f} | Php {php_amt:,.0f}".format(amt = amt, usd_amt = usd_amt, php_amt = php_amt)
          
		await message.channel.send(file=discord.File('images/SLP_50.png'))
		await message.channel.send(output_msg)
  
 	#Get SLP market price
	if msg.startswith("$axsprice"):
		usd_price, php_price, week_high, week_low = get_axs_price()
		output_msg = "Current Price: US$ {usd:.3f} | Php {php:.2f}\n7D Range: US$ {w_low:.3f}-{w_hi:.3f}".format(usd = usd_price, php = php_price, w_hi=week_high, w_low =week_low)
		if msg != "$axsprice":
		amt = int(msg.split("$axsprice ",1)[1])
		usd_amt = usd_price * amt
		php_amt = php_price * amt
		output_msg += "\n{amt} AXS = US$ {usd_amt:,.2f} | Php {php_amt:,.0f}".format(amt = amt, usd_amt = usd_amt, php_amt = php_amt)
			
		await message.channel.send(file=discord.File('images/axs_50.png'))
		await message.channel.send(output_msg)


client.run(bot_token)

