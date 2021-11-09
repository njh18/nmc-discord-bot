import discord
from API.getTokenPrice import getSLPPrice

def priceSLP(eth_logo, axs_logo, slp_logo, msg):  
  sgd_price, usd_price, php_price, eth_price, axs_price, week_high, week_low = getSLPPrice(
  )
  embed = discord.Embed(
      title="Smooth Love Potion ($SLP)", color=0xfe93a1
  ).set_thumbnail(
      url=
      'https://d235dzzkn2ryki.cloudfront.net/small-love-potion_large.png'
  )
  embed_msg = "🇺🇸 USD$ {usd:.3f} | 🇵🇭 PHP$ {php:.2f} | 🇸🇬 SGD$ {sgd:.3f} \n {eth_logo} ETH {eth:.8f} | {axs_logo} AXS {axs:.06f} \n".format(
      usd=usd_price,
      php=php_price,
      sgd=sgd_price,
      eth=eth_price,
      axs=axs_price,
      eth_logo=eth_logo,
      axs_logo=axs_logo)
  embed.add_field(name='Current Price', value=embed_msg, inline=False)
  embed.set_footer(text='💂 Hail Nephy.')
  if msg != "$priceslp":
      amt = int(msg.split("$priceslp ", 1)[1])
      amt_str = str(amt) + "SLP {slp_logo}".format(slp_logo=slp_logo)
      usd_amt = usd_price * amt
      php_amt = php_price * amt
      sgd_amt = sgd_price * amt
      axs_amt = axs_price * amt
      eth_amt = eth_price * amt
      embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} | 🇵🇭 PHP$ {php_amt:,.1f} \n ↳ {axs_logo} AXS {axs_amt:.6f} | {eth_logo} ETH {eth_amt:.8f}".format(
          sgd_amt=sgd_amt,
          usd_amt=usd_amt,
          php_amt=php_amt,
          axs_logo=axs_logo,
          axs_amt=axs_amt,
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