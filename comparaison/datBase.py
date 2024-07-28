import mysql.connector
import mysql 


def openConnection():

     db = mysql.connector.connect(
          host="localhost",
          user="smi",
          password="smi",
          database="test"
         )
     return db


def insertValues(columnsTuple,valTuple,tableName,db):
  try:
    cursor = db.cursor()
    sql = f"insert into {tableName}("
    for i in columnsTuple:
        sql+=str(i)+","
    sql=sql[:-1]
    sql+=") values("
    for i in valTuple:
        sql+=str(i)+","
    sql=sql[:-1]
    sql+=")"
    cursor.execute(sql)
    return True
  except Exception as e:
      print(e)
      return False

def getPlatforms():
    try:
        db = openConnection()
        cursor = db.cursor()
        sql = "select nom from platforme"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        return result
    except Exception as e:
        print(str(e))
        return []

def getPaires():
    try:
        db = openConnection()
        cursor = db.cursor()
        sql = "select  symbole from paire"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        return result
    except Exception as e:
        print(str(e))
        return []
    
def getTimeframe():
        result = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","1w"]
        return result
       
def truncateTable(tableName):
  try:
    db=openConnection()
    cursor = db.cursor()
    sql = f"delete from {tableName} where 1=1"
    cursor.execute(sql)
    db.commit()
    db.close()
    return True
  except:
      print("error during deleting values")
      return False

def selectData(platform,paire,timeframe,startDate,endDate):
   try :
      db=openConnection()
      cursor = db.cursor()
      sql = f"select timestamp,open,high,low,close,volume from {timeframe} where platform=(select id from platforme where nom='{platform}') and paire=(select id from paire where symbole='{paire}') and timestamp >= '{startDate}' and timestamp <= '{endDate}'"
      cursor.execute(sql)
      result = cursor.fetchall()
      db.commit()
      db.close()
      return result
   except Exception as e:
      # print(traceback.format_exc())
      return f"Error during selecting values: {str(e)}"
   


def paireExist(symbol,db):
    try:
      cursor = db.cursor()
      sql = f"select * from paire where symbole=\'{symbol}\'"
      cursor.execute(sql)
      result=cursor.fetchall()
      if len(result)==0:
         return False
      else: return True
    except Exception as e:
       print(str(e))
       return False
    
def dataExist(platform,symbol,timeframe,end,start):
   db= openConnection()
   sql=f"select timestamp from {timeframe} where platform=(select id from platforme where nom='{platform}') and paire=(select id from paire where symbole='{symbol}') and timestamp >= '{start}' and timestamp <= '{end}'"
   cursor=db.cursor()
   cursor.execute(sql)
   result=cursor.fetchall()
   if len(result)==0:
      db.close()
      return False
   db.close()
   return True


def platformExist(platform,db):
    try:
      cursor = db.cursor()
      sql = f"select * from platforme where nom=\'{platform}\'"
      cursor.execute(sql)
      result=cursor.fetchall()
      if len(result)==0:
         return False
      else: return True
    except Exception as e:
       print(str(e))
       return False
    
def insertingData(timestamp,open_price,heigh_price,low_price,close_price,volume,symbol,platform,timeframe,db):
    if platformExist(platform,db)==False:
       insertOneValue("nom",platform,"platforme",db)      
    if paireExist(symbol,db)==False:
       insertOneValue("symbole",symbol,"paire",db)
    vals = (f"\'{timestamp}\'",open_price,heigh_price,low_price, close_price,volume,f"(select id from paire where symbole=\'{symbol}\')",f"(select id from platforme where nom=\'{platform}\')")
    insertValues(("timestamp", "open", "high", "low", "close", "volume","paire","platform"),vals,timeframe,db)




def insertValues(columnsTuple,valTuple,tableName,db):
  try:
    cursor = db.cursor()
    sql = f"insert into {tableName}("
    for i in columnsTuple:
        sql+=str(i)+","
    sql=sql[:-1]
    sql+=") values("
    for i in valTuple:
        sql+=str(i)+","
    sql=sql[:-1]
    sql+=")"
    print(sql)
    cursor.execute(sql)
    db.commit()
    return True
  except Exception as e:
      print(e)
      return False

def insertOneValue(column,value,tableName,db):
  try:
    cursor = db.cursor()
    sql = f"insert into {tableName}({column}) values('{value}')"
    cursor.execute(sql)
    db.commit()
    return True
  except Exception as e:
      print(e)
      return False

# def readValues(columnTuple=("*"),tableName="1m",condition="1=1"):
#   #la fonction qui fait la selection des donnees dapres la base de donnees
#   try:
#       db=openConnection()
#       cursor = db.cursor()
#       sql = f"select "
#       for i in columnTuple:
#           sql+=f"{i}"+","
#       sql=sql[:-1]+f" from {tableName} where {condition}"
#       cursor.execute(sql)
#       result = cursor.fetchall()
#       db.commit()
#       db.close()
#       return result
#   except:
#       return "error during selecting values"

