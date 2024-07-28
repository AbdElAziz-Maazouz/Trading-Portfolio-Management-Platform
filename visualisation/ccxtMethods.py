import ccxt 
from datetime import datetime, timedelta
from calendar import *
import time
import ccxt.base.errors
import requests

bigTable = []
def getMarketDataKucoin1(symbol,timeframe,dateDebutTuple,dateFinTuple,platform):
  k=0
  if dateFinTuple<=dateDebutTuple:
      return bigTable
  else :
      if platform == "kucoin":
          exchange = ccxt.kucoin()
          max=1500
      elif platform=="bitstamp":
          exchange = ccxt.bitstamp()
          max=1000
      elif platform == "binance":
          exchange = ccxt.binance()
          max=500
      elif platform=="bittrex":
          exchange = ccxt.bittrex()
          max=1000
      elif platform=="coinbasepro":
          exchange = ccxt.coinbasepro()
          max=300
      elif platform=="kraken":
          exchange = ccxt.kraken()
          max=720
      if timeframe not in exchange.timeframes:
         print(f"timeframe not exist in {platform}")
         return []
      since = int(dateDebutTuple.timestamp()) * 1000
      try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=None, params={})
      except ccxt.errors.RateLimitExceeded as e:
          time.sleep(2)
          ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=None, params={})
      except requests.exceptions.RequestException:
         print("internet access denied")
         return []
      except ccxt.BadSymbol:
         print(f"symbol not supportable by {platform}")
         return []
      except ccxt.NetworkError:
         print("internet access is denied")
         return []
      for i in ohlcv:
          if datetime.fromtimestamp(i[0] / 1000.0) > dateDebutTuple and datetime.fromtimestamp(i[0] / 1000.0) <= dateFinTuple: 
             bigTable.append(i)

      if timeframe=="1s":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(seconds=max),dateFinTuple,platform)
      if timeframe=="1m":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(minutes=max),dateFinTuple,platform)
      elif timeframe=="3m":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(minutes=3*max),dateFinTuple,platform)
      elif timeframe=="5m":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(minutes=5*max),dateFinTuple,platform)
      elif timeframe=="15m":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(minutes=15*max),dateFinTuple,platform)
      elif timeframe=="30m":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(minutes=30*max),dateFinTuple,platform)
      elif timeframe=="1h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=max),dateFinTuple,platform)
      elif timeframe=="2h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=2*max),dateFinTuple,platform)
      elif timeframe=="4h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=4*max),dateFinTuple,platform)
      elif timeframe=="6h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=6*max),dateFinTuple,platform)
      elif timeframe=="8h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=8*max),dateFinTuple,platform)
      elif timeframe=="12h":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(hours=12*max),dateFinTuple,platform)
      elif timeframe=="1d":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(days=max),dateFinTuple,platform)
      elif timeframe=="3d":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(days=3*max),dateFinTuple,platform)
      elif timeframe=="1w":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(weeks=max),dateFinTuple,platform)
      elif timeframe=="2w":
        return getMarketDataKucoin1(symbol,timeframe,dateDebutTuple+timedelta(weeks=2*max),dateFinTuple,platform)



def clearTableData():
   bigTable.clear()