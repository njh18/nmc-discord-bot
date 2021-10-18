import os
import discord
from replit import db
from getFloorAxies import getFloorAxies
from criteriaBuilder import criteriaBuilder

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

	print(message.content)
	msg = message.content
	if msg.startswith('$floor-axies'):
		quote = getFloorAxies()
		await message.channel.send(quote)

	if msg.startswith('$search'):
		try:
			url = msg.split("$search ",1)[1]
			print(url)
		except IndexError:
			await message.channel.send("No Input given!")

client.run(bot_token)

# maybe can add into another folder or smt first then can join 

#but can only be online when i press run here LOL need to add to server eventually

#test can see me? nice didnt kno can do thisi have legacy code for slp tracker if need and send image

# can how to call into this? oh i saw