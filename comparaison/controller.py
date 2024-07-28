import ccxt
from comparaison.ajouterData import *
from comparaison.ccxtMethods import clearTableData, getMarketDataKucoin1
import datetime
import pandas as pd
from comparaison.datBase import *
from datetime import datetime
from comparaison.installing import *
DATA=[]

df_list = [] # create an empty list to store the dataframes

def sommeData(data1):
      global DATA
      if len(DATA)==0:
         print("hello")
         for k in data1:
            DATA.append(list(k))
         return DATA 
      else:
          DATA2=[]
          print("hello")
          print(len(data1))
          print(len(DATA))
          print(len(DATA2))
          for idx in range(len(data1)):
              if (len(DATA)!=0) and (len(data1)!=len(DATA)):
                  return DATA
            
              i = list(DATA[idx])
              j = list(data1[idx])
              if i[0]==j[0]:
                i[1]=i[1]+j[1]
                if i[2] < j[2]:
                    i[2]=j[2]
                if i[3] > j[3]:
                    i[3]=j[3]
                i[4]=i[4]+j[4]
                i[5]=i[5]+j[5]
 
              DATA2.append(i)
          DATA=DATA2[:]
      return DATA

def divisionData(num):
      global DATA
      for D in DATA:
        D[1]=D[1]/num
        D[4]=D[4]/num
      return DATA

def containTimeframeOrPaireOrDates(platform,paire,timeframe,start,end):
    data=selectData(platform,paire,timeframe,start,end)
    if len(data)==0:
        return False
    return True


def getDdataToShow(platform,paire,timeframe,startDate,endDate,pan):
      global DATA
      if platform !="All":
          if installerOuAfficher(paire,platform,timeframe,endDate,startDate)=="afficher":
                print("affichage../")
                data=selectData(platform,paire,timeframe,startDate,endDate)
                if len(data)==0:
                    pan.messagesLabel.setText("data not exist")
                    return []
                print(f"ehis is data : {data[0][0]}")
                result = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in data]  
                # Convert result to DataFrame
                df = pd.DataFrame(data=result, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
                df['Date'] = pd.to_datetime(df['Date'], format=f'%d/%m/%y %H:%M:%S')
                df.set_index("Date",inplace=True)
          elif installerOuAfficher(paire,platform,timeframe,endDate,startDate)=="installer":
                print("installation../")
                if searchAndSaveData(paire,timeframe,endDate,startDate,platform)==1:
                    data=selectData(platform,paire,timeframe,startDate,endDate)
                    print(data)
                    if len(data)==0:
                        pan.messagesLabel.setText("data not exist")
                        return []
                    result = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in data]  
                    # Convert result to DataFrame
                    df = pd.DataFrame(data=result, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
                    df['Date'] = pd.to_datetime(df['Date'], format=f'%d/%m/%y %H:%M:%S')
                    df.set_index("Date",inplace=True)
                # pan.pan1.hide()
                # pan.show()
      else:
          a=0
          for c in range(pan.platform.count()-1):
              if dataExist(pan.platform.itemText(c),paire,timeframe,endDate,startDate)==False:
                  continue
              else:
                a+=1
                platformi=str(pan.platform.itemText(c))
                print(platformi)
                data1=selectData(platformi,paire,timeframe,startDate,endDate)
                DATA=sommeData(data1)
          DATA=divisionData(a)
          del a
          result = [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in DATA]  
          # Convert result to DataFrame
          df = pd.DataFrame(data=result, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
          df['Date'] = pd.to_datetime(df['Date'], format=f'%d/%m/%y %H:%M:%S')
          df.set_index("Date",inplace=True)
          DATA.clear()
      return df

# def fillInComboBoxes(pan):
#    timeframes = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","1w"]
#    paires =["LINK/USDT","BTC/USDT","ETH/USDT","ADA/USDT","LTC/USDT","SOL/USDT","DOT/USDT","UNI/USDT"]
#    platforms = ["binance","kucoin","kraken","bittrex","bitstamp"]
#    for i in timeframes:
#        pan.timeframe.addItem(str(i))
#    for i in paires:
#        pan.paires.addItem(str(i))
#    for i in platforms:
#        pan.platform.addItem(str(i))
#    if len(platforms)>=2:
#      pan.platform.addItem("All")

def fillInComboBoxes(pan):
    platformes=["binance","kraken","bittrex","bitstamp","kucoin"]
    #2w 1s 1M 3d
    pan.platform.addItems(platformes)
    if len(ccxt.exchanges)>=2:
        pan.platform.addItem("All")
    exchange_name = pan.platform.currentText()
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class()
    markets = exchange.load_markets()
    paires = list(markets.keys())
    paires.sort()
    for i in paires:
        if "/USDT" in i:
            pan.paires.addItem(i)  
    timeframes = sorted(exchange.timeframes)
    for i in timeframes:
        if i!="1M":
            pan.timeframe.addItem(i)
   
def updatePaires(pan):
    if pan.platform.currentText()!="All":
        exchange_name = pan.platform.currentText()
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class()
        markets = exchange.load_markets()
        paires = list(markets.keys())
        paires.sort()
        print(len(paires))
        pan.paires.clear()
        for i in paires:
            if "/USDT" in i:
                pan.paires.addItem(i)  
        timeframes = exchange.timeframes
        pan.timeframe.clear()
        try:
            timeframes = exchange.timeframes
            for i in timeframes:
                if i!="1M":
                    pan.timeframe.addItem(i)
        except TypeError:
          pan.messagesLabel.setText("this platform is not available")

    
def installerOuAfficher(symbol,platform,timeframe,end,start):
    if dataExist(platform,symbol,timeframe,end,start)==True:
       return "afficher"
    else:
      return "installer"

       
def buttonAfficherClicked(pan):
    global df_list
    df_list.clear()
    dType=str(pan.DType.currentText())
    start=pan.startTime.dateTime().toPyDateTime()
    end  =pan.endTime.dateTime().toPyDateTime()
    timeframe = str(pan.timeframe.currentText())
    paire = str(pan.paires.currentText())
    platform = str(pan.platform.currentText())
    
    # if installerOuAfficher(paire,platform,timeframe,end,start)=="afficher":
    #     print("affichage...")
    if end<=start:
        pan.messagesLabel.setText("entrer un bon date")
        return 
    elif start<=datetime(2015,12,1,0,0,0):
        pan.messagesLabel.setText("entrez la date > 2015")
        return
    elif end > datetime.now():
        pan.messagesLabel.setText("date non correct ")
        return
    
    df = getDdataToShow(platform,paire,timeframe,start,end,pan)
    if len(df)>300 :
        pan.messagesLabel.setText("il y a autant des boujis (minimiser le rang) ")
        return
    if len(df)==0:
        pan.messagesLabel.setText("data pas existe")
        return
    
    df_list.append(df)
    pan.figure.df=df
    pan.figure.simplePlot(dType)

        

def buttonAjouterClick(pan):
    global df_list
    dType=str(pan.DType.currentText())
    start=pan.startTime.dateTime().toPyDateTime()
    end  =pan.endTime.dateTime().toPyDateTime()
    timeframe = str(pan.timeframe.currentText())
    paire = str(pan.paires.currentText())
    platform = str(pan.platform.currentText())
    
    # if installerOuAfficher(paire,platform,timeframe,end,start)=="afficher":
    #     print("affichage...")
    if end<=start:
        pan.messagesLabel.setText("entrer un bon date")
        return 
    elif start<=datetime(2015,12,1,0,0,0):
        pan.messagesLabel.setText("entrez la date > 2015")
        return
    elif end > datetime.now():
        pan.messagesLabel.setText("date non correct ")
        return
    
    df = getDdataToShow(platform,paire,timeframe,start,end,pan)
    if len(df)>300 :
        pan.messagesLabel.setText("il y a autant des boujis (minimiser le rang) ")
        return
    if len(df)==0:
        pan.messagesLabel.setText("data pas existe")
        return
    
    df_list.append(df)
    pan.figure.df_list=df_list
    pan.figure.AjoutPlot(dType)
    
    

# def buttonAppliquerClick(pan):
#     indicateur = str(pan.indicateurs.currentText())
#     periode = int(pan.indicateurPeriode.value())
#     if len(pan.figure.df) <= periode:
#         pan.messagesLabel.setText(" data ne contient pas cette periode")
#         return
#     if periode==1:
#         pan.messagesLabel.setText("choisissez une autre periode")
#         return
#     elif indicateur=="RSI":
#         pan.figure.setRsi(periode)
#     elif indicateur=="SMA":
#         pan.figure.setSma(periode)
#     elif indicateur=="WMA":
#         pan.figure.setWma(periode)


# def buttonRetourClick(pan):
#       pan.figure.deleteOne()
#       pan.figure.simplePlot()  


def searchAndSaveData(symbol,timeframe,dateDebutTuple,dateFinTuple,platform):
   print(f"debutTuple =  {dateDebutTuple}   finTuple={dateFinTuple}")
   dataa = getMarketDataKucoin1(symbol,timeframe,dateFinTuple,dateDebutTuple,platform)[:]
#    if datetime.fromtimestamp(dataa[0][0]-timestamp() / 1000.0)
   clearTableData()
   print(dataa)
   db=openConnection()
   for i in dataa:
     if datetime.fromtimestamp(i[0] / 1000.0) <= dateDebutTuple:
        timestamp=datetime.fromtimestamp(i[0] / 1000.0).strftime(f'%Y-%m-%d %H:%M:%S')
        open_price = i[1]
        heigh_price=i[2]
        low_price=i[3]
        close_price=i[4]
        volume=i[5]
        db=openConnection()
        insertingData(timestamp,open_price,heigh_price,low_price,close_price,volume,symbol,platform,timeframe,db)
   db.commit()
   db.close()
   return 1