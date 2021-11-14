import discord
from API.getAxieSaleTotal import getAxieSaleTotal
from API.getAxiePrice import getAxiePrice
from API.getPriceTrend import getPriceTrend
from replit import db

def cronJobNumber1(client):
  eth_logo = 0
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
      
  embed.add_field(name="# of Axies on Sale", value=getAxieSaleTotal(), inline=False)
  for key in db["filters"]:
      name, url, eth_cost, usd_cost = getAxiePrice(key)
      msg = "{eth_logo} ETH {eth:.3f} | ".format(eth_logo=eth_logo,
          eth=eth_cost) + "🇺🇸US$ {usd:.0f} ".format(
              usd=usd_cost) + "\n [Link to the marketplace]({url})".format(
                  url=url)
      embed.add_field(name=name, value=msg, inline=False)
      getPriceTrend(key)

  return channel, embed