from config import *

'''
Each module must receive **kwargs as a parameter. The kwargs variable is a dictionary
consisting of all the data extracted from the probe request. Each module name must
start with 'alert_' and have a matching variable in config.py for enabling/disabling.
Configurable module options may be defined in config.py.
'''

from email.mime.text import MIMEText
import smtplib

def alert_sms(**kwargs):
    msg = MIMEText('WUDS proximity alert! A foreign device (%s - %s) has been detected on the premises.' % (kwargs['bssid'], kwargs['oui']))
    server = smtplib.SMTP(SMTP_SERVER)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SMTP_USERNAME, SMS_EMAIL, msg.as_string())
    server.quit()

import urllib
# import urllib2 
# todo: replace library call with urllib.request or whatever
import requests
import json

def alert_pushover(**kwargs):
    msg = 'Proximity alert! A foreign device (%s - %s) has been detected on the premises.' % (kwargs['bssid'], kwargs['oui'])
    url = 'https://api.pushover.net/1/messages.json'
    payload = {'token': PUSHOVER_API_KEY, 'user': PUSHOVER_USER_KEY, 'message': msg}
    payload = urllib.parse.urlencode(payload)
    resp = urllib.requests.urlopen(url, data=payload)

def alert_telegram(**kwargs):
    msg = 'Proximity alert! A foreign device (%s - %s) has been detected on the premises.' % (kwargs['bssid'], kwargs['oui'])
    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID)
    payload = {'text': msg}
    payload = urllib.parse.urlencode(payload)
    resp = urllib.requests.urlopen(url, data=payload)

def alert_pushbullet(**kwargs):
    msg = 'Proximity alert! A foreign device (%s - %s) has been detected on the premises.' % (kwargs['bssid'], kwargs['oui'])
    url = 'https://api.pushbullet.com/v2/pushes'
    payload = {'type': 'note', 'title': 'WUDS', 'body': msg}
    payload = json.dumps(payload)
    resp = requests.post(url, data=payload, headers={'Authorization': 'Bearer ' + PUSHBULLET_API_KEY, 'Content-Type': 'application/json'})
