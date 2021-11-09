import discord
from replit import db
from API.getAxiePrice import getAxiePrice


def forceAP(eth_logo):  
  embed = discord.Embed(title="Axie Prices",
                        description="Average axie prices in ETH and US$",
                        color=discord.Color.random())
  embed.set_thumbnail(
      url=
      "https://s.alicdn.com/@sc04/kf/H6ff5bea9b74745a790b7c41afdd61cdbl.png"
  )
  for key in db["filters"]:
      name, url, eth_cost, usd_cost = getAxiePrice(key)
      msg = str(eth_logo) + "ETH {eth:.3f} | ".format(
          eth=eth_cost) + "🇺🇸US$ {usd:.0f} ".format(
              usd=usd_cost
          ) + "\n [Link to the marketplace]({url})".format(url=url)
      embed.add_field(name=name, value=msg, inline=False)
  return embed