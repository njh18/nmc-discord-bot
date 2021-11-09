import discord
from API.getTokenPrice import getETHPrice

def priceETH(eth_logo, axs_logo, slp_logo, msg):
  sgd_price, usd_price, php_price, slp_price, axs_price, week_high, week_low = getETHPrice(
  )
  embed = discord.Embed(
      title="Ethereum ($ETH)", color=0x627eea).set_thumbnail(
          url='https://i.ibb.co/y5NBSd2/eth-logo-1.png')
  embed_msg = "🇺🇸 USD$ {usd:.0f} | 🇵🇭 PHP$ {php:.0f} | 🇸🇬 SGD$ {sgd:.0f} \n {slp_logo} SLP {slp:.0f} | {axs_logo} AXS {axs:.0f} \n".format(
      usd=usd_price,
      php=php_price,
      sgd=sgd_price,
      slp=slp_price,
      axs=axs_price,
      slp_logo=slp_logo,
      axs_logo=axs_logo)
  embed.add_field(name='Current Price', value=embed_msg, inline=False)
  embed.set_footer(text='💂 Hail Nephy.')
  if msg != "$priceeth":
      amt = float(msg.split("$priceeth ", 1)[1])
      amt_str = str(amt) + " ETH {eth_logo}".format(eth_logo=eth_logo)
      usd_amt = usd_price * amt
      php_amt = php_price * amt
      sgd_amt = sgd_price * amt
      axs_amt = axs_price * amt
      slp_amt = slp_price * amt
      embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.0f} | 🇸🇬 SGD {sgd_amt:,.0f} | 🇵🇭 PHP$ {php_amt:,.0f} \n ↳ {axs_logo} AXS {axs_amt:.2f} | {slp_logo} SLP {slp_amt:.0f}".format(
          sgd_amt=sgd_amt,
          usd_amt=usd_amt,
          php_amt=php_amt,
          axs_logo=axs_logo,
          axs_amt=axs_amt,
          slp_logo=slp_logo,
          slp_amt=slp_amt)
      embed.add_field(name=amt_str, value=embed_msg2, inline=False)
  else:
      embed.add_field(name="7-Day Price Range",
                      value="🇺🇸 USD$ {w_low:.2f}-{w_hi:.2f}".format(
                          usd=usd_price, w_hi=week_high, w_low=week_low))

  return embed 