from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
import smtplib
import ssl
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

smtp_port = 587
smtp_server = "smtp.gmail.com"
message = " hello world "
email_from="khadersha.sk@gmail.com"
pswd="ytubdbhnanjepczp"
from datetime import date

today = date.today()
def mail( message, email_to ):
    simple_email_context = ssl.create_default_context()
    try:
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        TIE_server.sendmail(email_from, email_to, message)
        print("adding appointment")
        print("message sent successfully")
    except Exception as e:
        print(e)

def extract_details(text):
    if (","in text):
        textl=text.split(",")
    else:
        textl=text.split(" ")
    patient_name=textl[0]
    date=textl[1]
    doctor=textl[2]
    hospital=text[3]
    email=textl[4]

    add_appointment(patient_name,date ,doctor ,hospital,email)
        
def add_appointment(patient_name, date, doctor, hospital, email):
    filenumber_p = int(os.listdir('appointments')[-1])
    filenumber_p = filenumber_p+1
    with open('appointments/' + str(filenumber_p), "w+") as file:
        with open('template.txt', 'r') as source_file:
            lines = source_file.readlines()
            output_string = ''.join(lines)
            formatted_output_string = output_string.format(patient_name=patient_name, date=date, doctor=doctor, hospital=hospital, email=email)
            file.write(formatted_output_string)
    with open('appointments/' + str(filenumber_p), 'r') as file:
        message = file.read()
    
    mail(message, email)
filenumber = int(os.listdir('saved_conversations')[-1])
filenumber = filenumber+1
file = open('saved_conversations/'+str(filenumber), "w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

app = Flask(__name__)
english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile = os.listdir('saved_conversations')[-1]
    appendfile = open('saved_conversations/'+str(filenumber), "a")
    if(("Patient Name" in userText) or ("Doctor" in userText) or ("@gmail" in userText)):
     
        extract_details(userText)
        
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response

if __name__ == "__main__":
    app.run(debug=True)
