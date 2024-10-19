#importing modules
import speech_recognition as sr
import pyttsx3
import mysql.connector
import pyperclip
import time

#Globals
Stat = "loggedout"
user = "hello"

#Creating the database;
mydb = mysql.connector.connect(host="localhost",user="root",passwd="12345678")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS csproj;")

#Creating the table;
mydb = mysql.connector.connect(host="localhost",user="root",passwd="12345678",database="csproj")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS userdata (uname VARCHAR(255) PRIMARY KEY, passwd VARCHAR(255) NOT NULL);")
mycursor.execute("CREATE TABLE IF NOT EXISTS data (id INT PRIMARY KEY auto_increment, website_name VARCHAR(255) NOT NULL, email_username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, username VARCHAR(255), FOREIGN KEY (username) REFERENCES userdata(uname));")

#function for talk
engine = pyttsx3.init()
engine.setProperty('rate',160)
def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    listener = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                print("hearing...")
                listener.adjust_for_ambient_noise(mic, duration=0.6)
                audio = listener.listen(mic)
                text = listener.recognize_google(audio)
                text = text.lower()

                print(f"Recognized text {text}")
                return text
            
        except sr.UnknownValueError:
            listener = sr.Recognizer()
            continue

def register():
    talk("Tell your username no speacial charecters allowed")
    time.sleep(2)
    uname = get_audio()
    uname = uname.replace(" ","")
    print(uname)
    talk("Enter your password in the screen")
    time.sleep(2)
    passwd = input("Enter the Password: ")
    query = "INSERT INTO userdata (uname,passwd) VALUES('%s','%s')"%(uname,passwd,)
    mycursor.execute(query)
    mydb.commit()

def login():
    global user
    talk("tell the username to login")
    time.sleep(2)
    uname = get_audio()
    uname = uname.replace(" ","")
    talk("Enter your password in the screen")
    time.sleep(2)
    passwd = input("Enter the Password: ")
    query = "SELECT * FROM userdata WHERE uname= '%s' AND passwd = '%s'"%(uname,passwd)
    mycursor.execute(query)
    if mycursor.fetchall():
        global Stat
        a="Login successful" + "  welcome  " + uname
        Stat = "loggedin"
        user = uname
        talk(a)
        time.sleep(1)
    else:
        talk("Login failed")
        time.sleep(1)

def adds():
    global user
    talk("Tell the website name you wish to add")
    time.sleep(2)
    s = get_audio()
    talk("Enter the site username/email")
    time.sleep(2)
    usr = input("Enter The username: ")
    passwdr = input("Enter the password: ")
    query = "INSERT INTO data (website_name, email_username, password, username) VALUES ('%s','%s','%s','%s')"%(s,usr,passwdr,user)
    mycursor.execute(query)
    mydb.commit()

def fetch():
    l = []
    global user
    talk("Tell the name of the site for which you want the password")
    time.sleep(2)
    web = get_audio()
    query = "SELECT email_username , password FROM data WHERE username = '%s' AND website_name = '%s'"%(user,web)
    mycursor.execute(query)
    a = mycursor.fetchall()
    for i in a:
        for j in i:
            l.append(j)
    print("Username/Email is: ",l[0])
    pyperclip.copy(l[0])
    talk("Username copied to clipboard sir")
    time.sleep(10)
    talk("Password copied to clipboard sir")
    pyperclip.copy(l[1])

def delete():
    global user
    talk("Tell the name of the site which you want to delete")
    time.sleep(2)
    web = get_audio()
    query = "DELETE FROM data WHERE username = '%s' AND website_name = '%s'"%(user,web)
    mycursor.execute(query)
    mydb.commit()
    if mycursor.rowcount == 0:
        talk("Sorry sir, no such record exsists")
        time.sleep(2)
    else:
        talk("Deleted successfully sir")

def modify():
    global user
    talk("Tell the name of the site which you want to update")
    time.sleep(2)
    web = get_audio()
    talk("Enter the username and password")
    time.sleep(2)
    usr = input("Enter the Username/E-mail: ")
    pwd = input('Enter the new password: ')
    query = "UPDATE data set email_username='%s' WHERE username = '%s' AND website_name = '%s'"%(usr,user,web)
    query1 = "UPDATE data set password='%s' WHERE username = '%s' AND website_name = '%s'"%(pwd,user,web)
    mycursor.execute(query)
    mycursor.execute(query1)
    mydb.commit()

def logout():
    global Stat, user
    Stat = "loggedout"
    user = ""

def rmuser():
    talk("Tell The username to remove the user")
    time.sleep(2)
    usr = get_audio()
    usr = usr.replace(" ","")
    talk("Please enter the password to confirm it's you")
    time.sleep(2)
    ped = input("Password: ")
    query = "DELETE FROM userdata WHERE uname='%s' AND passwd='%s'"%(usr,ped)
    mycursor.execute(query)
    mydb.commit()
    talk("User removed successfully")
    time.sleep(1)

while True:
    if Stat=='loggedout':
        talk("Do you want to Login or Register or Delete user or exit the application sir")
        time.sleep(2)
        command=get_audio()
        if 'login' in command:
            login()
        if 'register' in command:
            register()
        if 'delete' in command:
            rmuser()
        if 'exit' in command:
            break
    if Stat=='loggedin':
        talk("Do you want to Create or Get or Modify or Delete or logout sir")
        time.sleep(2)
        command = get_audio()
        if 'create' in command:
            adds()
        if 'delete' in command:
            delete()
        if 'modify' in command:
            modify()
        if 'get' in command:
            fetch()
        if 'logout' in command:
            logout()
        if 'bye' in command:
            logout()
            break
        if 'exit' in command:
            logout()
            break
