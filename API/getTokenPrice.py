import os
import json
import requests
from pycoingecko import CoinGeckoAPI
from forex_python.converter import CurrencyRates

cg = CoinGeckoAPI()
print(cg.ping())
fx = CurrencyRates()

def getSLPPrice():
  slp_price = cg.get_price("smooth-love-potion", ("sgd, usd, php, eth"))
  sgd_price = slp_price['smooth-love-potion']['sgd']
  usd_price = slp_price['smooth-love-potion']['usd']
  php_price = slp_price['smooth-love-potion']['php']
  eth_price = slp_price['smooth-love-potion']['eth']
  axs_price = cg.get_price("smooth-love-potion", ("eth"))['smooth-love-potion']['eth']/cg.get_price("axie-infinity", ("eth"))['axie-infinity']['eth']
  hist_price = (cg.get_coin_ohlc_by_id("smooth-love-potion", "usd", 7))
  week_high = max([el[2] for el in hist_price])
  week_low = min([el[3] for el in hist_price])
  return (sgd_price,usd_price,php_price,eth_price,axs_price,week_high,week_low)

def getETHPrice():
  eth_price = cg.get_price("ethereum", ("sgd, usd, php"))
  sgd_price = eth_price['ethereum']['sgd']
  usd_price = eth_price['ethereum']['usd']
  php_price = eth_price['ethereum']['php']
  slp_price = 1/cg.get_price("smooth-love-potion", ("eth"))['smooth-love-potion']['eth']
  axs_price = 1/cg.get_price("axie-infinity", ("eth"))['axie-infinity']['eth']
  hist_price = (cg.get_coin_ohlc_by_id("ethereum", "usd", 7))
  week_high = max([el[2] for el in hist_price])
  week_low = min([el[3] for el in hist_price])
  return (sgd_price,usd_price,php_price,slp_price,axs_price,week_high,week_low)

def getAXSPrice():
  axs_price = cg.get_price("axie-infinity", ("sgd, usd, php, eth"))
  sgd_price = axs_price['axie-infinity']['sgd']
  usd_price = axs_price['axie-infinity']['usd']
  php_price = axs_price['axie-infinity']['php']
  eth_price = axs_price['axie-infinity']['eth']
  slp_price = cg.get_price("axie-infinity", ("eth"))['axie-infinity']['eth']/cg.get_price("smooth-love-potion", ("eth"))['smooth-love-potion']['eth']
  hist_price = (cg.get_coin_ohlc_by_id("axie-infinity", "usd", 7))
  week_high = max([el[2] for el in hist_price])
  week_low = min([el[3] for el in hist_price])
  return (sgd_price,usd_price,php_price,eth_price,slp_price,week_high,week_low)

def getSgdPrice():
  sgd_price = cg.get_price("xsgd", ("usd, php, eth"))
  # eth_price = 1/cg.get_price("eth", ("sgd"))
  slp_price = 1/cg.get_price("smooth-love-potion", ("sgd"))['smooth-love-potion']['sgd']
  axs_price = 1/cg.get_price("axie-infinity", ("sgd"))['axie-infinity']['sgd']
  usd_price = sgd_price['xsgd']['usd']
  php_price = sgd_price['xsgd']['php']
  eth_price = sgd_price['xsgd']['eth']
  return usd_price,php_price,eth_price,axs_price,slp_price

def getPhpPrice():
  php_price = cg.get_price("xphp", ("usd, sgd, eth"))
  # eth_price = 1/cg.get_price("eth", ("sgd"))
  slp_price = 1/cg.get_price("smooth-love-potion", ("php"))['smooth-love-potion']['php']
  axs_price = 1/cg.get_price("axie-infinity", ("php"))['axie-infinity']['php']
  # usd_price = php_price'xphp']['usd']
  usd_price = fx.get_rate("PHP", "USD",None)
  # sgd_price = php_price['xphp']['sgd']
  sgd_price = fx.get_rate("PHP", "SGD",None)
  # eth_price = php_price['xphp']['eth']
  eth_price = 1/cg.get_price("ethereum", ("php"))['ethereum']['php']
  return usd_price,sgd_price,eth_price,axs_price,slp_price

def getUsdPrice():
  usd_price = cg.get_price("usdt", ("sgd, php, eth"))
  # eth_price = 1/cg.get_price("eth", ("sgd"))
  slp_price = 1/cg.get_price("smooth-love-potion", ("usd"))['smooth-love-potion']['usd']
  axs_price = 1/cg.get_price("axie-infinity", ("usd"))['axie-infinity']['usd']
  # sgd_price = usd_price['tether']['sgd']
  sgd_price = fx.get_rate("USD", "SGD",None)
  print(sgd_price)
  print(type(sgd_price))
  # php_price = usd_price['usdt']['php']
  php_price = fx.get_rate("USD", "PHP",None)
  print(type(php_price))
  # eth_price = usd_price['usdt']['eth']
  eth_price = 1/cg.get_price("ethereum", ("usd"))['ethereum']['usd']
  return sgd_price,php_price,eth_price,axs_price,slp_price