import mysql.connector


#cnx = mysql.connector.connect(user="ltrsoft", password="Amol@2019", host="ltrdbserver.mysql.database.azure.com", port=3306, database="question", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
cnx = mysql.connector.connect(user="kiran", password="Kale@2002", host="read.mysql.database.azure.com", port=3306, database="smart", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
print(cnx)

mycursor = cnx.cursor()
#mycursor.execute("DROP TABLE voice")
#mycursor.execute("CREATE TABLE user (id int primary key AUTO_INCREMENT,fname VARCHAR(255),lname VARCHAR(255),email VARCHAR(255),username VARCHAR(255),password VARCHAR(255),address VARCHAR(255))")
#mycursor.execute("CREATE TABLE  (id int primary key AUTO_INCREMENT,mname VARCHAR(255),cname VARCHAR(255),context VARCHAR(255),usedfor VARCHAR(255))")
#sql = "INSERT INTO user (username,password) VALUES (%s,%s)"
#sql = "INSERT INTO medicine (id,mname,cname,context,usedfor) VALUES (%s, %s,%s,%s, %s)"
#val = ("karpude ","karpude123")
#mycursor.execute(sql, val)

#cnx.commit()

#print(mycursor.rowcount, "record inserted.")

#mycursor.execute(sql)
#mycursor.execute("CREATE TABLE voice (id int primary key AUTO_INCREMENT,fname VARCHAR(255),lname VARCHAR(255),email VARCHAR(255),username VARCHAR(255),password VARCHAR(255),address VARCHAR(255))")
#mycursor.execute("CREATE TABLE voice (id int primary key AUTO_INCREMENT,fname VARCHAR(255),lname VARCHAR(255),email VARCHAR(255),username VARCHAR(255),password VARCHAR(255),address VARCHAR(255))")

sql = "DELETE FROM user WHERE username= %s"
adr = ("abc",)
mycursor.execute(sql, adr)
cnx.commit()
print(mycursor.rowcount, "record(s) deleted")

mycursor.execute("SELECT username,password FROM user")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


#mycursor.execute("SELECT id,mname,cname,context,usedfor FROM medicine")

#myresult = mycursor.fetchall()

#for x in myresult:
 # print(x)
