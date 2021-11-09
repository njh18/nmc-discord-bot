import discord
from API.getTokenPrice import getAXSPrice

def priceAXS(eth_logo, axs_logo, slp_logo, msg):
  sgd_price, usd_price, php_price, eth_price, slp_price, week_high, week_low = getAXSPrice(
  )
  embed = discord.Embed(
      title="Axie Infinity Coin ($AXS)", color=0x01befe
  ).set_thumbnail(
      url=
      'https://seeklogo.com/images/A/axie-infinity-axs-logo-57FE26A5DC-seeklogo.com.png'
  )
  embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} | 🇸🇬 SGD$ {sgd:.3f} \n {eth_logo} ETH {eth:.8f} | {slp_logo} SLP {slp:.0f} \n".format(
      usd=usd_price,
      php=php_price,
      sgd=sgd_price,
      eth=eth_price,
      slp=slp_price,
      eth_logo=eth_logo,
      slp_logo=slp_logo)
  embed.add_field(name='Current Price', value=embed_msg, inline=False)
  embed.set_footer(text='💂 Hail Nephy.')
  if msg != "$priceaxs":
      amt = float(msg.split("$priceaxs ", 1)[1])
      amt_str = str(amt) + " AXS {axs_logo}".format(axs_logo=axs_logo)
      usd_amt = usd_price * amt
      php_amt = php_price * amt
      sgd_amt = sgd_price * amt
      slp_amt = slp_price * amt
      eth_amt = eth_price * amt
      embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.0f}\n ↳ 🇸🇬 SGD$ {sgd:.3f} | ".format(
          usd_amt=usd_amt, php_amt=php_amt,
          sgd=sgd_amt) + str(eth_logo) + "ETH {eth_amt:,.4f}".format(
              eth_amt=eth_amt)
      embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.1f} \n ↳ {slp_logo} SLP {slp_amt:.0f} | {eth_logo} ETH {eth_amt:.4f}".format(
          sgd_amt=sgd_amt,
          usd_amt=usd_amt,
          php_amt=php_amt,
          slp_logo=slp_logo,
          slp_amt=slp_amt,
          eth_logo=eth_logo,
          eth_amt=eth_amt)
      embed.add_field(name=amt_str, value=embed_msg2, inline=False)
  else:
      embed.add_field(name="7-Day Price Range",
                      value="🇺🇸 USD$ {w_low:.2f}-{w_hi:.2f}".format(
                          usd=usd_price,
                          php=php_price,
                          w_hi=week_high,
                          w_low=week_low)) 

  return embed 