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



def clientExist(cin):
     db=openConnection()
     sql=f"select * from client where cin='{cin}'"
     cursor=db.cursor()
     cursor.execute(sql)
     result = cursor.fetchall()
     if len(result)==0:
          db.close()
          return False
     else :
          db.close()
          return True

def trueInfos(cin,password):
     db=openConnection()
     sql=f"select password from client where cin='{cin}'"
     cursor=db.cursor()
     cursor.execute(sql)
     result = cursor.fetchall()
     if result[0][0]==password:
          db.close()
          return True
     else:
          db.close()
          return False
     
def getInfos(cin):
     db=openConnection()
     sql=f"select nom,prenom,email,telephone,password,cin,id from client where cin='{cin}'"
     cursor=db.cursor()
     cursor.execute(sql)
     result = cursor.fetchall()
     db.close()
     return result


def insertClient(cin,nom,prenom,phone,mail,password):
     db=openConnection()
     sql=f"insert into client(nom,prenom,email,telephone,cin,password) values('{nom}','{prenom}','{mail}','{phone}','{cin}','{password}')"
     cursor=db.cursor()
     cursor.execute(sql)
     db.commit()
     db.close()

def apiExist(cin,key,platforme):
     db=openConnection()
     sql = f"select * from api where idClient=(select id from client where cin='{cin}') and idPlatforme=(select id from platforme where nom='{platforme}')"
     cursor=db.cursor()
     cursor.execute(sql)
     result = cursor.fetchall()
     if len(result)==0:
          db.close()
          return False
     else:
          db.close()
          return True

def ajouterApiMethod(cin,key,secret,platforme):
     print(key,"  ",secret)
     db=openConnection()
     sql = f"insert into api(api_key,api_secret,idClient,idPlatforme) values('{key}','{secret}',(select id from client where cin='{cin}'),(select id from platforme where nom='{platforme}'))"
     cursor=db.cursor()
     cursor.execute(sql)
     db.commit()
     db.close()

def modifierApiMethod(cin,key,secret,platforme):
     db=openConnection()
     sql = f"update api set api_key='{key}' and api_secret='{secret}' where idClient=(select id from client where cin='{cin}') and idPlatforme=(select id from platforme where nom='{platforme}')"
     cursor=db.cursor()
     cursor.execute(sql)
     db.commit()
     db.close()

def platformExist(platforme):
     db=openConnection()
     sql = f"select id from platforme where nom='{platforme}'"
     cursor=db.cursor()
     cursor.execute(sql)
     result = cursor.fetchall()
     if len(result)==0:
          db.close()
          return False
     else:
          db.close()
          return True
def ajouterPlatforme(platforme):
     db=openConnection()
     sql = f"insert into platforme(nom) values('{platforme}')"
     cursor=db.cursor()
     cursor.execute(sql)
     db.commit()
     db.close()
