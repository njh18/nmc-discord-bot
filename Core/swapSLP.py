import discord
import asyncio
from API.getTokenPrice import getSLPPrice

async def swapSLP(message, eth_logo, axs_logo):
  sgd_price, usd_price, php_price, eth_price, axs_price, week_high, week_low = getSLPPrice(
  )
  currency_logos = ['🇸🇬', '🇺🇸', '🇵🇭', eth_logo, axs_logo]
  currency_names = ['SGD', 'USD', 'PHP', 'ETH', 'AXS']

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
      if message.content != "$swapslp":
          amt = float(message.content.split("$swapslp ", 1)[1])
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
      if message.content != "$swapslpr":
          amt = float(message.content.split("$swapslp ", 1)[1])
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
      if message.content != "$swapslp":
          amt = float(message.content.split("$swapslp ", 1)[1])
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
      if message.content != "$swapslp":
          amt = float(message.content.split("$swapslp ", 1)[1])
          amt_str = str(amt) + " SLP"
          eth_amt = eth_price * amt
          embed_msg2 = " ↳ ETH {eth_amt:,.2f}".format(amt=amt,
                                                      eth_amt=eth_amt)
          embed.add_field(name=amt_str, value=embed_msg2, inline=False)
      await message.channel.send(embed=embed)
      
  if (currency == 'AXS'):
      embed = discord.Embed(
          title="Smooth Love Potion ($SLP)", color=0xfe93a1
      ).set_thumbnail(
          url=
          'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
      )
      embed_msg = "AXS {axs:.8f}".format(axs=axs_price)
      embed.add_field(name='Current Price',
                      value=embed_msg,
                      inline=False)
      embed.set_footer(text='💂 Hail Nephy.')
      if message.content != "$swapslp":
          amt = float(message.content.split("$swapslp ", 1)[1])
          amt_str = str(amt) + " SLP"
          axs_amt = axs_price * amt
          embed_msg2 = " ↳ AXS {axs_amt:,.2f}".format(amt=amt,
                                                      axs_amt=axs_amt)
          embed.add_field(name=amt_str, value=embed_msg2, inline=False)
      await message.channel.send(embed=embed)