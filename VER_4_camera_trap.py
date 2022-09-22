import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from time import sleep
import time
# Importowanie modułów do wysyłania poczty
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json

#nadawca = 
#haslo = 
#odbiorca  = 

DIR = './Camera_trap/'
FILE_PREFIX = 'image'
            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  # Odczytaj wyjście z czujnika ruchu PIR

def email():
    print( 'wysylanie e-maila')
    # utwórz ściezke jesli nieistnieje
    if not os.path.exists(DIR):
        os.makedirs(DIR)
   # Znajdź największy identyfikator istniejących obrazów.
   # Rozpocznij nowe obrazy po tej wartości identyfikatora.
    pliki = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
    count = 0  #jak jet w pliku np 10 zdjecie  to nastepne ma pokazac 11
    
    if len(pliki) > 0:
        # Pobierz licznik od ostatniej nazwy pliku.
        count = int(pliki[-1][-7:-4])+1

    #zapisz obraz do pliku
    nazwa_pliku = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % count)
    today=datetime.today()
    konvert_date=today.strftime("%c")
    # złap twarz
    json_date={"date":[konvert_date],"nazwa_pliku":[nazwa_pliku]} 
    #json_date={"date":konvert_date,"nazwa_pliku":nazwa_pliku}
    data=json.dumps(json_date,indent=2, sort_keys=True,default=str)
    with picamera.PiCamera() as camera:
        pic = camera.capture(nazwa_pliku)
    # wysylanie emaila
    
    
      
    '''    
    for konvert_date in json_date:
                        json_date.append(nazwa_pliku)
                        json_date.append(konvert_date)
                      
    for x,y in json_date.items():
        json_date.update()
    '''                  
   
   


       
    with open("logi.json","w") as f:
        new_date=json.dumps(json_date,indent=2, sort_keys=True,default=str)
        
    '''   
    with open("logi2.json","w") as f2:
           json.dumps(new_date)
    '''
    '''
    with open("logi.json","w") as f:
        json.dump(json_date,f)
        
    with open("logi.json","a") as f:
        new_date=json.dumps(json_date,indent=2, sort_keys=True,default=str)

          
               for x,y in json_date.items():
                    json_date.update({"date":konvert_date,"photo":nazwa_pliku})
    
    print(new_date)  
    '''
    '''
    msg = MIMEMultipart()
    msg['From'] = nadawca
    msg['To'] = odbiorca
    msg['Subject'] = 'wykrycie ruchu'  
    
    body = 'zdjęcie jest w załączniku'  #wiadomosc przeslana na email
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(nazwa_pliku, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % nazwa_pliku)
    msg.attach(part)
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(nadawca, haslo)
    text = msg.as_string()
    server.sendmail(nadawca, odbiorca, text)
    server.quit()
    '''
    

while True:    
    i = GPIO.input(11)
    if i == 0:  #Gdy sygnał wyjściowy z czujnika ruchu jest NISKI
        print('nie ma intruzów', i)
        sleep(0.3)
    elif i == 1:  # Gdy sygnał wyjściowy z czujnika ruchu jest WYSOKI
        print (" pojawił się intruz", i)
        #todaysDate = datetime.today();
        #print("Today's date - Using date class:%s"%todaysDate);
      
        email()
        

 
