import os
import mysql.connector
import PyPDF3
import azure.cognitiveservices.speech as sdk
import requests

cnx = mysql.connector.connect(user="Vedant", password="Nogja@2004", host="mysql1249.mysql.database.azure.com",
                              port=3306, database="smart_reader", ssl_ca="DigiCertGlobalRootCA.crt.pem",
                              ssl_disabled=False)
print(cnx)
print("Welcome to Smart Reader")
ch1 = 1
ch = 0


def login():
    username = input("Enter your Username:")
    password = input("Enter your PassWord:")

    mycursor = cnx.cursor()

    sql = "SELECT username,password FROM user WHERE username = %s and password=%s"
    adr = (username, password)

    mycursor.execute(sql, adr)

    myresult = mycursor.fetchall()

    if len(myresult) == 1:
        print("Successfully login")
        return True
    else:
        print("Login failed")
        return False
    return True


def register():
    print("Please fill registration deatils:")
    mycursor = cnx.cursor()
    mycursor.execute("SELECT id FROM user")

    myresult = mycursor.fetchall()
    id = 0
    for x in myresult:
        id = x

    fname = input("Enter Your First Name:")
    lname = input("Enter Your Last Name:")
    email = input("Enter Your Email:")
    username = input("Enter Your User Name:")
    password = input("Enter Your password:")
    cpassword = input("Enter Confirm password:")
    address = input("Enter Your First Name:")
    if (password == cpassword):
        sql = "INSERT INTO user (id,fname,lname,email,username,password,address) VALUES (%s, %s,%s,%s, %s,%s,%s)"
        val = (str(id + 1), fname, lname, email, username, password, address)
        mycursor.execute(sql, val)
        cnx.commit()
        print(mycursor.rowcount, "You have successfully register")
    else:
        password = input("Enter Your password:")
        cpassword = input("Enter Confirm password:")
        sql = "INSERT INTO user (id,fname,lname,email,username,password,address) VALUES (%s, %s,%s,%s, %s,%s,%s)"
        val = (str(id + 1), fname, lname, email, username, password, address)
        mycursor.execute(sql, val)
        cnx.commit()
        print(mycursor.rowcount, "You have successfully register")


def pdfreader():
    key = "08118a610f8d40cf844e9f0e3d252fbe"  # make sure to replace this with your own API key
    region = "centralindia"  # make sure to replace this with your own service region
    source_language = "en-US"
    target_language = "mr"
    endpoint = "https://ltr.cognitiveservices.azure.com/"

    config = sdk.SpeechConfig(subscription=key, region=region)
    synthesizer = sdk.SpeechSynthesizer(speech_config=config)
    filename=input("Enter File name:")
    book = open(filename, "rb")
    reader = PyPDF3.PdfFileReader(book)
    # print(book)

    for num in range(0, reader.numPages):
        text = reader.getPage(num).extractText()
        result = synthesizer.speak_text_async(text).get()
        print(text)
    translate(text, source_language, target_language, key, region, endpoint)


def translate(text, source_language, target_language, key, region, endpoint):
    # Use the Translator translate function
    url = endpoint + '/translate'
    # Build the request
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': target_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]
    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    # Get translation
    translation = response[0]["translations"][0]["text"]
    # Return the translation

    print()

    return translation


while ch1 == 1:
    print("Menu:")
    print("1.Login")
    print("2.Register")
    ch = int(input("Enter your choice:"))
    if ch == 1:
        print("Enter Login Credential")
        l = login()
        if (l):
            print("Menu:")
            print("1.Open pdf for reading")

            ch = int(input("Enter your choice:"))
            if (ch == 1):

                pdfreader()
                break

        else:
            print("Login failed")

    if (ch == 2):
        print("User Regitration")
        register()
        break
