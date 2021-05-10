import requests
from email.mime.text import MIMEText
from datetime import date
import smtplib, sys
from datetime import datetime
import time
import subprocess

dtime = datetime.now().strftime("%d-%m-%Y")

#Set frequency with seconds to check vaccine availablity
frequency = 60
# set PINCODE below with 6 digit numeric value
PINCODE = ["560010","560002","560008","560011","560020","560008","560003","560001","560076","560078","560066","560060","560041","560043","560064"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
#set your personal gmail address, make sure you allow less secure application to use gmail ..
#    To enable less secure app 
#    Go to the Less secure app access section of your Google Account. You might need to sign in.
#    Turn Allow less secure apps ON.

SMTP_USERNAME = "********@gmail.com"
SMTP_PASSWORD = "********"
EMAIL_FROM = "*******@gmail.com"

# specify list of comma seprated email address in double quotes
EMAIL_TO = ["********@gmail.com"]
# specify your email address 

DATE_FORMAT = "%d/%m/%Y"
EMAIL_SPACE = ", "

DATA='This is the vaccine status check..'

def send_email(sub, emailTolist):
    msg = MIMEText(DATA)
    msg['Subject'] = sub + " %s" % (date.today().strftime(DATE_FORMAT))
    msg['To'] = EMAIL_SPACE.join(emailTolist)
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, emailTolist, msg.as_string())
    mail.quit()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

while (True):
    try:
        for eachpin in PINCODE:
            print ("Trying at cowin site at PINCODE :  " + eachpin +  "\nAt ::  " + str(datetime.now().strftime("%H:%M:%S")))
            weburl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + eachpin +  "&date=" + dtime
            r =requests.get(weburl, headers=headers)
            res = r.json()
            centers = res['centers']
            #print (centers)
            for cen in centers:
                
                for ses in cen['sessions']:
                    if ses['min_age_limit'] < 19:
                        print ("Location----------------:     " + cen['address'])
                        print ("available_capacity------:     " + str(ses['available_capacity']))
                        if ses['available_capacity'] > 0:
                            sub = "Covax update: Avaiable at : " + cen['address']
                            send_email(sub, EMAIL_TO)
                            print ("Vaccine available, mail sent")
                            subprocess.call("osascript -e '{}'".format(sub), shell=True)
        print ("\n\nNo vaccine available.... trying after " + str(frequency) + " seconds\n\n")
        print ("---------------------------------------------------------------")
        time.sleep(frequency)
    except:
        print ("\n.......  Some exception occured.... continuing.. \n")
        pass
