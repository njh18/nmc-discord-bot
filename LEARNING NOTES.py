import discord


client = discord.Client();

@client.event
async def on_member_join(member):
	print(f'{member} has joined a server')

@client.event
async def on_member_remove(member):
	print(f'{member} has left a server')

