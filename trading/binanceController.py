
import time
import schedule
import ccxt





balances = None
prev_balances = None


def getTotal(balances):
    total = sum(balances[currency]["price"]*balances[currency]["quantity"] for currency in balances)
    return total

def sell(exchange,currency, amount,markets):
    global balances
    if currency in balances:
        if balances[currency]["sell"]=="n":
            return 0
        if balances[currency]["sell"]=="Y":
            print("##################################   boom  #########################################")
            amount=(balances[currency]["price"]*balances[currency]["quantity"])/10
        balances[currency]["quantity"] = balances.get(currency, {}).get("quantity", 0) - (amount / balances[currency].get("price", 1))
        balances['USDT']["quantity"] = balances['USDT']["quantity"] + amount
        return amount
    return 0

def buy(exchange,currency, amount,markets):
    global balances
    if currency in balances:
        if balances[currency]["buy"]=="n" or balances["USDT"]["buy"]=="n":
            return 0 
        balances[currency]["quantity"] = balances.get(currency, {}).get("quantity", 0) + (amount / balances[currency].get("price", 1))
        balances['USDT']["quantity"] = balances['USDT']["quantity"] - amount
        return amount
    return 0


def getPercent(currency, balances,total):
    if currency in balances:
        percentage = ((balances[currency]["quantity"]*balances[currency]["price"]) / total) * 100
        return percentage
    else:
        return None
    


def sort(currencies,balances,prev_balances):
    print("sorting")
    # if (getPercent(currency, prev_balances) * getTotal(balances) / 100) > (getPercent(currency, balances) * getTotal(balances) / 100):
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
            # if (balances[currency]["price"]*balances[currency]["quantity"]) <= (prev_balances[currency]["price"]*prev_balances[currency]["quantity"]):
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
   



def setBalances(exchange,currencies,capitales):
    global balances
    if balances==None:
        balances = {currency: {"price":0,"quantity":0,"buy":"y","sell":"y"} for currency in currencies}
        for currency,cap in zip(currencies,capitales):
            if currency!="USDT":
                ticker = exchange.fetch_ticker(currency+"/"+"USDT")
                balances[currency]["price"]=ticker['last']
                balances[currency]["quantity"]=cap/balances[currency]["price"]
            else:
                balances[currency]["price"]=1
                balances[currency]["quantity"]=cap
    else:
        # balances = {currency: {"price":0,"quantity":0,"buy":"y","sell":"y"} for currency in currencies}
        for currency in currencies:
            if currency!="USDT":
                ticker = exchange.fetch_ticker(currency+"/"+"USDT")
                balances[currency]["price"]=ticker['last']
    # print(f"balances=============>>>>>> {balances}")
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


def trade(exchange,currencies,markets,capitales,indicatorOfSell,limitOfUsdt):
    global first_total
    global benifit
    global compte_bancaire
    transaction_benifit=0
    global first_balances
    global balances
    global increaseOrDecrease
    balances=setBalances(exchange,currencies,capitales)
    global prev_balances
    if first_balances==None:
        first_balances=balances
    # print(" fb ",first_balances)
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
                prev_percent=getPercent(currency,prev_balances,prev_total)
                percent=getPercent(currency,balances,prev_total)
                variationIndicatorOfSell=increaseOrDecrease[currency]
                p=percent-prev_percent
                if p<0:
                    buy_amount=p*prev_total/100

                    b=buy(exchange,currency, -buy_amount,markets)
                    print(f"buy: {currency} {b}$ ")
                    transaction_benifit-=b
                elif p>0:
                    sell_amount = p*prev_total/100
                    s=sell(exchange,currency, sell_amount,markets)  
                    print(f"sell: {currency} {s}$  increase={variationIndicatorOfSell}%")
                    transaction_benifit+=s 
        else :
            for currency in sorted_currencies:
                if currency=="USDT":
                    continue
                prev_percent=getPercent(currency,prev_balances,total)
                percent=getPercent(currency,balances,total)
                variationIndicatorOfSell=increaseOrDecrease[currency]
                # if (balances[currency]["price"]*balances[currency]["quantity"]) <= (prev_balances[currency]["price"]*prev_balances[currency]["quantity"]):
                p=percent-prev_percent
                if p<0:
                    buy_amount=p*total/100
                    b=buy(exchange,currency, -buy_amount,markets)
                    print(f"buy: {currency} {b}$ ")
                    transaction_benifit-=b
                elif p>0:
                    sell_amount = p*total/100
                    s=sell(exchange,currency, sell_amount,markets)  
                    print(f"sell: {currency} {s}$  increase={variationIndicatorOfSell}%")
                    transaction_benifit+=s   
    print(f"exchange benifit: {transaction_benifit}$")
    if transaction_benifit>0:
        if increaseOrDecrease["USDT"]>=0:
            balances["USDT"]["quantity"]-=0.2*transaction_benifit
            compte_bancaire+=0.2*transaction_benifit

    
    if prev_balances and compte_bancaire>0:
        benifit=(getTotal(balances)+compte_bancaire)-first_total
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




def startbinance(exch,curr):
    global exchange
    global currencies
    # global markets
    currencies=curr
    exchange = exch
    # markets= exchange.load_markets()
    schedule.every(1).seconds.do(trade)
    while True:
        schedule.run_pending()
        