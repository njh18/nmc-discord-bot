import os
import json
import requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
print(cg.ping())

def get_slp_price():
  slp_price = cg.get_price("smooth-love-potion", ("usd, php"))
  usd_price = slp_price['smooth-love-potion']['usd']
  php_price = slp_price['smooth-love-potion']['php']
  hist_price = (cg.get_coin_ohlc_by_id("smooth-love-potion", "usd", 7))
  week_high = max([el[2] for el in hist_price])
  week_low = min([el[3] for el in hist_price])
  return (usd_price,php_price,week_high,week_low)

def get_axs_price():
  axs_price = cg.get_price("axie-infinity", ("usd, php"))
  usd_price = axs_price['axie-infinity']['usd']
  php_price = axs_price['axie-infinity']['php']
  hist_price = (cg.get_coin_ohlc_by_id("axie-infinity", "usd", 7))
  week_high = max([el[2] for el in hist_price])
  week_low = min([el[3] for el in hist_price])
  return (usd_price,php_price,week_high,week_low)