import discord
from API.getTokenPrice import getUsdPrice

def priceUSD(eth_logo, axs_logo, slp_logo, msg):
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

  return embed