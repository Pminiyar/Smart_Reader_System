
import tkinter as tk
from tkinter import END, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk  # pip install pillow
from tkinter.filedialog import askdirectory

import os
import mysql.connector
import PyPDF3
import azure.cognitiveservices.speech as sdk
import requests

import azure.cognitiveservices.speech as speechsdk


cnx = mysql.connector.connect(user="Vedant", password="Nogja@2004", host="mysql1249.mysql.database.azure.com",
                              port=3306, database="smart_reader", ssl_ca="DigiCertGlobalRootCA.crt.pem",
                              ssl_disabled=False)

mycursor = cnx.cursor()

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        
        border = tk.LabelFrame(self, text='Login', bg='ivory', bd = 10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx = 150, pady=150)

        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width = 30, bd = 5)
        T1.place(x=180, y=20)

        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='ivory')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width = 30, show='*', bd = 5)
        T2.place(x=180, y=80)

        def verify():

            username = T1.get()
            password = T2.get()



            sql = "SELECT username,password FROM user WHERE username = %s and password=%s"
            adr = (username, password)

            mycursor.execute(sql, adr)

            myresult = mycursor.fetchall()

            if len(myresult) == 1:
                controller.show_frame(SecondPage)
                messagebox.showinfo(" Successfully login !!")
                # print("Successfully login")
                return True
            else:
                messagebox.showinfo("Error", "Please provide correct username and password!!")
                return False
            return True

        B1 = tk.Button(border, text="Submit", font=("Arial", 15), command=verify)
        B1.place(x=320, y=115)
        
        def register():
            window = tk.Tk()
            window.resizable(0,0)
            window.configure(bg="deep sky blue")
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial",15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 200, y=10)
            
            l2 = tk.Label(window, text="Password:", font=("Arial",15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x = 200, y=60)
            
            l3 = tk.Label(window, text="Confirm Password:", font=("Arial",15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x = 200, y=110)
            
            def check():

                if t1.get()!="" or t2.get()!="" or t3.get()!="":
                    if t2.get()==t3.get():
                        username = t1.get()
                        password = t2.get()
                        sql = "INSERT INTO user (username,password) VALUES (%s,%s)"
                        # sql = "INSERT INTO medicine (id,mname,cname,context,usedfor) VALUES (%s, %s,%s,%s, %s)"
                        val = (username, password)
                        mycursor.execute(sql, val)

                        cnx.commit()
                #         with open("credential.txt", "a") as f:
                #             f.write(t1.get()+","+t2.get()+"\n")
                        messagebox.showinfo("Welcome","You are registered successfully!!")
                    else:
                        messagebox.showinfo("Error","Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                    
            b1 = tk.Button(window, text="Sign in", font=("Arial",15), bg="#ffc22a", command=check)
            b1.place(x=170, y=150)
            
            window.geometry("470x220")
            window.mainloop()
            
        B2 = tk.Button(self, text="Register", bg = "dark orange", font=("Arial",15), command=register)
        B2.place(x=650, y=20)
        
class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
        
        def select():
            # filepath=filedialog.askopenfilename(initialdir="F:\\MRDOCTOR\\login form",title="openfile",filetypes=(("text","*.txt"),("PDF","*.pptx"),("all files","*.*")))
            # file=open(filepath,'rb')
            # print(file.read())
            # file.close()

            key = "08118a610f8d40cf844e9f0e3d252fbe"  # make sure to replace this with your own API key
            region = "centralindia"  # make sure to replace this with your own service region
            source_language = "en-US"
            target_language = "mr"
            endpoint = "https://ltr.cognitiveservices.azure.com/"

            config = sdk.SpeechConfig(subscription=key, region=region)
            synthesizer = sdk.SpeechSynthesizer(speech_config=config)
            filepath=filedialog.askopenfilename(initialdir="F:\\MRDOCTOR\\login form",title="openfile",filetypes=(("PDF","*.pdf"),("all files","*.*")))

            book = open(filepath, "rb")
            print(filepath)
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

        B3 = tk.Button(self, text="Select PDF ", bg = "dark orange", font=("Arial",15), command=select)
        B3.place(x=300, y=200)
   
        
        
       
        

        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        window.grid_rowconfigure(0, minsize = 500)
        window.grid_columnconfigure(0, minsize = 800)
        
        self.frames = {}
        for F in (FirstPage, SecondPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(FirstPage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")
            
app = Application()
app.maxsize(800,500)
app.mainloop()
 