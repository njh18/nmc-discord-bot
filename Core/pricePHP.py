import discord
from API.getTokenPrice import getPhpPrice

def pricePHP(eth_logo, axs_logo, slp_logo, msg):
  usd_price, sgd_price, eth_price, axs_price, slp_price = getPhpPrice()

  embed = discord.Embed(
      title="Phillipines Pesos ($PHP)", color=0x766572).set_thumbnail(
          url="https://i.ibb.co/ThcC6TM/Mask-Group-4.png")
  embed_msg = "🇺🇸 USD$ {usd:.2f} | 🇸🇬 SGD$ {sgd:.2f} \n {eth_logo} ETH {eth:.6f} | {axs_logo} AXS {axs:.4f} | {slp_logo} SLP {slp:.2f}".format(
      sgd=sgd_price,
      usd=usd_price,
      eth=eth_price,
      axs=axs_price,
      slp=slp_price,
      eth_logo=eth_logo,
      axs_logo=axs_logo,
      slp_logo=slp_logo)
  embed.add_field(name='Current Price', value=embed_msg, inline=False)
  embed.set_footer(text='💂 Hail Nephy.')
  if msg != "$pricephp":
      amt = int(msg.split("$pricephp ", 1)[1])
      amt_str = str(amt) + " PHP"
      usd_amt = usd_price * amt
      sgd_amt = sgd_price * amt
      axs_amt = axs_price * amt
      eth_amt = eth_price * amt
      slp_amt = slp_price * amt
      embed_msg2 = " ↳ 🇺🇸 USD$ {usd_amt:,.2f} | 🇸🇬 SGD {sgd_amt:,.2f} \n ↳ {eth_logo} ETH {eth_amt:,.4f} | {axs_logo} AXS {axs_amt:.4f} | {slp_logo} SLP {slp_amt:.2f}".format(
          sgd_amt=sgd_amt,
          usd_amt=usd_amt,
          eth_amt=eth_amt,
          eth_logo=eth_logo,
          axs_logo=axs_logo,
          axs_amt=axs_amt,
          slp_logo=slp_logo,
          slp_amt=slp_amt)
      # embed_msg2 = " ↳ USD$ {usd_amt:,.2f} | SGD {sgd_amt:,.0f} | SLP {slp_amt:.0f}\n ↳ ETH$ {eth_amt:.5f} | AXS {axs_amt:.3f}".format(usd_amt = usd_amt, sgd_amt = sgd_amt,slp_amt=slp_amt,eth_amt=eth_amt,axs_amt=axs_amt)
      embed.add_field(name=amt_str, value=embed_msg2, inline=False) 

  return embed 