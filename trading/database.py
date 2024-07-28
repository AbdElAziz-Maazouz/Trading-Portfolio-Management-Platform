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

def getIdOfCin(cin):
     db=openConnection()
     sql = f"select id from client where cin='{cin}'"
     cursor=db.cursor()
     cursor.execute(sql)
     id = cursor.fetchall()
     return id[0][0]
    #  return 1

def getApisOfUser(id):
     db=openConnection()
     sql = f"select idPlatforme from api where idClient={id}"
     
     cursor=db.cursor()
     cursor.execute(sql)
     idPlatfrome = cursor.fetchall()
     new_list = [t[0] for t in idPlatfrome]
     return new_list


def getPlatfromeById(idp):
     db=openConnection()
     sql = f"select nom from platforme where id={idp}"
     
     cursor=db.cursor()
     cursor.execute(sql)
     platforme = cursor.fetchall()
     return platforme[0][0]

def getNomPlatformesApi(cin):
     idc = getIdOfCin(cin)
     print(f"idClient={idc}")
     idapis = getApisOfUser(idc)
     print(f"idsApis={idapis}")
     platformes = []
     if idapis==[]:
       return platformes
     for i in idapis:
          platformes.append(getPlatfromeById(i))
          print(f"platformes:{platformes}")
     return platformes

def getApiOfPlatformeAndUser(platforme,cin):
     db=openConnection()
     sql = f"select api_key,api_secret from api where idPlatforme=(select id from platforme where nom ='{platforme}' and idClient=(select id from client where cin='{cin}'))"
     cursor=db.cursor()
     cursor.execute(sql)
     api = cursor.fetchall()
     print(list(api[0]))
     return list(list(api[0]))
     