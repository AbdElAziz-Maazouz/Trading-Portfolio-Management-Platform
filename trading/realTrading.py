
import time
import schedule
import ccxt





balances = None
prev_balances = None


def getTotal(balances):
    total = sum(balances[currency]["price"]*balances[currency]["quantity"] for currency in balances)
    return total

def sell(exchange,currency, dollars,limits,markets):
    global balances
    if currency in balances:
        if balances[currency]["sell"]=="n":
            return 0
        if balances[currency]["sell"]=="Y":
            print("##################################     #########################################")
            dollars=(balances[currency]["price"]*balances[currency]["quantity"])/10
    market = markets[currency+"/"+"USDT"]
    min_amount = market['limits']['amount']['min']
    max_amount = market['limits']['amount']['max']
    ticker = exchange.fetch_ticker(currency+"/USDT")
    price = ticker['last']
    print(f"SELL {dollars} $ oF {currency}")
    amount=dollars/price
    if amount*price<float(limits):
            try:
              nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=(float(limits)/price)+amount+0.1,side='sell')
              nativeOrder=exchange.create_market_buy_order(currency+"/USDT",(float(limits)/price)+0.1)
            except Exception as e:
                return 0
            return dollars
    elif amount <= max_amount and amount>=min_amount:
         try:
           nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount,side='sell')
           return dollars
         except ccxt.InvalidOrder as e:
             if "MARKET_LOT_SIZE" in str(e):
                 nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount/2,side='sell')
                 nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount/2,side='sell')
                 return dollars
         except Exception as e:
                return 0
    elif amount >= max_amount:
        k=0
        while amount>min_amount :
            for i in range(1,100):
                k=amount/i
                if k>max_amount :
                    continue
                try:
                  nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=k,side='sell')
                except Exception as e:
                    continue
                amount=amount-k
                break
            continue
        return dollars
    elif amount<=min_amount:
            print(amount,"$")
            print(min_amount,"$")
            try:
               nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=min_amount+amount,side='sell')
               nativeOrder=exchange.create_market_buy_order(currency+"/USDT",min_amount)
            except Exception as e:
                return 0            
            return dollars


def buy(exchange,currency, dollars,limits,markets):
    global balances
    if currency in balances:
        if balances[currency]["buy"]=="n" or balances["USDT"]["buy"]=="n":
            return 0 
    market = markets[currency+"/"+"USDT"]
    min_amount = market['limits']['amount']['min']
    max_amount = market['limits']['amount']['max']
    ticker = exchange.fetch_ticker(currency+"/USDT")
    price = ticker['last']
    print(f"BUY {dollars} $ oF {currency}")
    amount=dollars/price
    if amount*price<float(limits):
            nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=(float(limits)/price)+amount+0.1,side='buy')
            nativeOrder=exchange.create_market_sell_order(currency+"/USDT",(float(limits)/price)+0.1)
            return dollars
    elif amount <= max_amount and amount>=min_amount:
         try:
           nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount,side='buy')
           return dollars
         except ccxt.InvalidOrder as e:
             if "MARKET_LOT_SIZE" in str(e):
                 nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount/2,side='buy')
                 nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=amount/2,side='buy')
                 return dollars
    elif amount >= max_amount:
        k=0
        while amount>min_amount :
            for i in range(1,100):
                k=amount/i
                if k>max_amount :
                    continue
                nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=k,side='buy')
                amount=amount-k
                break
            continue
        return dollars
    elif amount<=min_amount:
            print(amount,"$")
            print(min_amount,"$")
            nativeOrder=exchange.create_market_order(symbol=currency+"/USDT",amount=min_amount+amount,side='buy')
            nativeOrder=exchange.create_market_sell_order(currency+"/USDT",min_amount)
            return dollars




def getPercent(currency, balances,total):
    if currency in balances:
        percentage = ((balances[currency]["quantity"]*balances[currency]["price"]) / total) * 100
        return percentage
    else:
        return None
    

def sort(currencies,balances,prev_balances):
    print("sorting")
    sorted_currencies = []
    buyed = []
    prev_total=getTotal(prev_balances)
    total=getTotal(balances)
    if total >= prev_total:
        for currency in currencies:
            prev_percent=getPercent(currency,prev_balances,prev_total)
            percent=getPercent(currency,balances,prev_total)
            p=percent-prev_percent
            if p<=0:
                buyed.append(currency)
            elif p>0:
                sorted_currencies.append(currency) 
    else :
        for currency in currencies:
            prev_percent=getPercent(currency,prev_balances,total)
            percent=getPercent(currency,balances,total)
            p=percent-prev_percent
            if p<=0:
                buyed.append(currency)
            elif p>0:
                sorted_currencies.append(currency)
    print(f"buyed: {buyed}")
    print(f"selled: {sorted_currencies}")
    for i in buyed:
      sorted_currencies.append(i)
    sorted_currencies.append("USDT")
    return sorted_currencies





def setBalances(exchange,currencies):
    global balances
    b=exchange.fetch_balance()
    k=0
    if balances==None:
        balances = {currency: {"price":0,"quantity":0,"buy":"y","sell":"y"} for currency in currencies}
    for currency in currencies:
        if currency!="USDT":
            ticker = exchange.fetch_ticker(currency+"/"+"USDT")
            balances[currency]["price"]=ticker['last']
            balances[currency]["quantity"]=b['free'][currency]
            k+=balances[currency]["quantity"]
        
    balances["USDT"]["price"]=1
    balances["USDT"]["quantity"]=b['free'][currency]-k

    return balances




first_total=None
compte_bancaire = 0
benifit=0
increaseOrDecrease = None
first_balances=None

def getIncreasingOrDecreasing(currencies,indicatorOfSell,limitOfUsdt):
    global increaseOrDecrease
    global prev_balances
    global first_balances
    global balances
    if increaseOrDecrease==None:
       increaseOrDecrease = {currency: 0 for currency in currencies}
    for currency in currencies:
        if currency=="USDT":
            diffrence=balances[currency]["quantity"]-prev_balances[currency]["quantity"]
            increaseOrDecrease[currency]+=(diffrence*100)/prev_balances[currency]["quantity"]
            if increaseOrDecrease[currency]<limitOfUsdt:
                balances[currency]["buy"]="n"
                balances[currency]["sell"]="y"       
        else:  
            diffrence=balances[currency]["price"]-prev_balances[currency]["price"]
            increaseOrDecrease[currency]+=(diffrence*100)/prev_balances[currency]["price"]
            if increaseOrDecrease[currency]>=0:
                balances[currency]["buy"]="y"
                balances[currency]["sell"]="y"
            if increaseOrDecrease[currency]<0:
                balances[currency]["buy"]="y"
                balances[currency]["sell"]="n"
            if increaseOrDecrease[currency]>indicatorOfSell:
                balances[currency]["buy"]="n"
                balances[currency]["sell"]="Y"
            if prev_balances[currency]["sell"]=="n" and ((diffrence*100)/prev_balances[currency]["price"])>0:
                balances[currency]["buy"]="n"
                balances[currency]["sell"]="Y"
    return increaseOrDecrease


def tradeReal(exchange,currencies,markets,capitales,indicatorOfSell,limitOfUsdt):
    global first_total
    global benifit
    global compte_bancaire
    transaction_benifit=0
    global first_balances
    global balances
    global increaseOrDecrease
    balances=setBalances(exchange,currencies)
    global prev_balances
    if first_balances==None:
        first_balances=balances
    if first_total==None:
       first_total=getTotal(balances)
    total_balance = getTotal(balances) 
    print(f'Updated total balance is: {total_balance}')
    print(balances)
    if prev_balances :
        increaseOrDecrease=getIncreasingOrDecreasing(currencies,indicatorOfSell,limitOfUsdt)
        sorted_currencies = sort(currencies,balances,prev_balances)
        prev_total=getTotal(prev_balances)
        total=getTotal(balances)
        print(sorted_currencies)
        if total >= prev_total:
            for currency in sorted_currencies:
                if currency=="USDT":
                    continue
                limits = exchange.markets[currency+"/"+"USDT"]['info']['filters'][6]['minNotional']
                prev_percent=getPercent(currency,prev_balances,prev_total)
                percent=getPercent(currency,balances,prev_total)
                variationIndicatorOfSell=increaseOrDecrease[currency]
                p=percent-prev_percent
                if p<0:
                    buy_amount=p*prev_total/100

                    b=buy(exchange,currency, -buy_amount,limits,markets)
                    print(f"buy: {currency} {b}$ ")
                    transaction_benifit-=b
                elif p>0:
                    sell_amount = p*prev_total/100
                    s=sell(exchange,currency, sell_amount,limits,markets)  
                    print(f"sell: {currency} {s}$  increase={variationIndicatorOfSell}%")
                    transaction_benifit+=s 

        else :
            for currency in sorted_currencies:
                if currency=="USDT":
                    continue
                limits = exchange.markets[currency+"/"+"USDT"]['info']['filters'][6]['minNotional']
                prev_percent=getPercent(currency,prev_balances,total)
                percent=getPercent(currency,balances,total)
                variationIndicatorOfSell=increaseOrDecrease[currency]
                p=percent-prev_percent
                if p<0:
                    buy_amount=p*total/100
                    b=buy(exchange,currency, -buy_amount,limits,markets)
                    print(f"buy: {currency} {b}$ ")
                    transaction_benifit-=b
                elif p>0:
                    sell_amount = p*total/100
                    s=sell(exchange,currency, sell_amount,limits,markets)  
                    print(f"sell: {currency} {s}$  increase={variationIndicatorOfSell}%")
                    transaction_benifit+=s   

    balances=setBalances(exchange,currencies)
    print(f"exchange benifit: {transaction_benifit}$")
    if transaction_benifit>0:
        if increaseOrDecrease["USDT"]>=0:
          compte_bancaire+=0.2*transaction_benifit

    
    if prev_balances and compte_bancaire>0:
        benifit=(getTotal(balances))-first_total
    benifitPercentage=0
    if prev_balances and compte_bancaire>0:
      benifitPercentage = (benifit*100)/first_total

    print(f"banque: {compte_bancaire} $")
    print("your benifit = ",benifit," $")
    values = []
    usdt=0
    total=0
    if prev_balances==None:
        prev_balances = {currency: {"price":0,"quantity":0,"buy":"y","sell":"y"} for currency in currencies}
    for currency in currencies:
        if currency!="USDT":
          percentage=getPercent(currency, balances,getTotal(balances))
          values.append([(balances[currency]["price"]*balances[currency]["quantity"]),balances[currency]["price"],percentage])
        if currency in balances:
          prev_balances[currency]["price"] = balances[currency]["price"]
          prev_balances[currency]["quantity"] = balances[currency]["quantity"]
          prev_balances[currency]["buy"] = balances[currency]["buy"]
          prev_balances[currency]["sell"] = balances[currency]["sell"]
        else:
            print("NONE")

    usdt = balances["USDT"]["quantity"]
    total=getTotal(balances)
    print("\n")
    results=[total,usdt,values,compte_bancaire,100+benifitPercentage]
    return results


