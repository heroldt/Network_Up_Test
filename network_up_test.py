import os
import csv
from datetime import datetime, timedelta
import requests

dt_today = datetime.now()
dt_yesterday = dt_today - timedelta(1)
date_today = "%04i%02i%02i" %(dt_today.year,dt_today.month,dt_today.day) 
hostname_gateway = "fritz.box"
hostname_wifi = ""
hostname_extern = "google.com"
filename_today = "network_test_%04i%02i%02i.csv" % (dt_today.year,dt_today.month,dt_today.day) 
filename_yesterday = "network_test_%04i%02i%02i.csv" % (dt_yesterday.year,dt_yesterday.month,dt_yesterday.day)
filename_telegram_log = "telegram_log.csv" 
gateway_up_cnt = 0
wifi_up_cnt = 0
extern_up_cnt = 0
check_cnt = 0

bot_token = ""
bot_ID = ""

def ping(hostname):
    return os.system("ping -c 1 " + hostname)

def print_summary():
  print("Gateway: %i (%.f%%)" %(gateway_up_cnt,gateway_up_cnt/check_cnt*100))
  print("Wifi: %i (%.f%%)" %(wifi_up_cnt,wifi_up_cnt/check_cnt*100))
  print("Extern: %i (%.f%%)" %(extern_up_cnt,extern_up_cnt/check_cnt*100))

def check_network():
  with open(filename_today,"a") as csvfile:
    csv_writer = csv.writer(csvfile)

    if os.stat(filename_today).st_size == 0:
      csv_writer.writerow(['time','gateway','wifi','extern'])
    
    gateway_check = 'nOK'
    wifi_check = 'nOK'
    extern_check = 'nOK'
    if ping(hostname_gateway) == 0:
      gateway_check = 'OK'
    if ping(hostname_wifi) == 0:
      wifi_check = 'OK'
    if ping(hostname_extern) == 0:
      extern_check = 'OK'

    csv_writer.writerow(["%02i:%02i:%02i" % (dt_today.hour,dt_today.minute,dt_today.second),gateway_check,wifi_check,extern_check])

def read_csv(filename):
  global gateway_up_cnt
  global wifi_up_cnt
  global extern_up_cnt
  global check_cnt

  gateway_up_cnt = 0
  wifi_up_cnt = 0
  extern_up_cnt = 0
  check_cnt = 0

  try:
    with open(filename,"r") as csvfile:
      csv_reader = csv.reader(csvfile)
      next(csv_reader) #skip first line (header)
      for row in csv_reader:
        if row[1] == 'OK':
          gateway_up_cnt += 1
        if row[2] == 'OK':
          wifi_up_cnt += 1
        if row[3] == 'OK':
          extern_up_cnt += 1
        check_cnt += 1
    return True
  except:
    return False

def get_daily_summary():
  title_text = "Zusammenfassung für gestern %02i.%02i.%i:\n" %(dt_yesterday.day,dt_yesterday.month,dt_yesterday.year)
  if check_cnt == gateway_up_cnt and check_cnt == wifi_up_cnt and check_cnt == extern_up_cnt:
    summary_text = "Gestern gab es keine Ausfälle!"
  else:
    summary_text = "Gateway: %i (%.f%%)\nWifi: %i (%.f%%)\nExtern: %i (%.f%%)" %(
      gateway_up_cnt,gateway_up_cnt/check_cnt*100,wifi_up_cnt,wifi_up_cnt/check_cnt*100,extern_up_cnt,extern_up_cnt/check_cnt*100)
  return title_text + summary_text

def send_message(message):
  send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_ID + '&parse_mode=Markdown&text=' + message
  response = requests.get(send_text)
  set_telegram_log(filename_telegram_log)
  return response.json()

def set_telegram_log(filename):
  with open(filename,"a") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([date_today,"%02i:%02i:%02i" %(dt_today.hour,dt_today.minute,dt_today.second)])

def get_telegram_log(filename):
  try:
    with open(filename,"r") as csvfile:
      csv_reader = csv.reader(csvfile)
      for row in csv_reader:
        if row[0] == date_today:
          return True
      return False
  except:
    return False

if __name__ == "__main__":
  check_network()
  read_csv(filename_today)
  print_summary()
  if True == read_csv(filename_yesterday) and False == get_telegram_log(filename_telegram_log):
    send_message(get_daily_summary())