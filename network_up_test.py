import os
import csv
from datetime import datetime
import requests

dt = datetime.now()
hostname_gateway = "fritz.box"
hostname_wifi = ""
hostname_extern = "google.com"
filename = "network_test_%04i%02i%02i.csv" % (dt.year,dt.month,dt.day) 
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
  with open(filename,"a") as csvfile:
    csv_writer = csv.writer(csvfile)

    if os.stat(filename).st_size == 0:
      csv_writer.writerow(['date','gateway','wifi','extern'])
    
    gateway_check = 'nOK'
    wifi_check = 'nOK'
    extern_check = 'nOK'
    if ping(hostname_gateway) == 0:
      gateway_check = 'OK'
    if ping(hostname_wifi) == 0:
      wifi_check = 'OK'
    if ping(hostname_extern) == 0:
      extern_check = 'OK'

      csv_writer.writerow(["%02i:%02i:%02i" % (dt.hour,dt.minute,dt.second),gateway_check,wifi_check,extern_check])

def read_csv():
  global gateway_up_cnt
  global wifi_up_cnt
  global extern_up_cnt
  global check_cnt

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

def get_daily_summary():
  title_text = "Zusammenfassung für gestern %02i.%02i.%i:\n" %(dt.day,dt.month,dt.year)
  if check_cnt == gateway_up_cnt and check_cnt == wifi_up_cnt and check_cnt == extern_up_cnt:
    summary_text = "Gestern gab es keine Ausfälle!"
  else:
    summary_text = "Gateway: %i (%.f%%)\nWifi: %i (%.f%%)\nExtern: %i (%.f%%)" %(
      gateway_up_cnt,gateway_up_cnt/check_cnt*100,wifi_up_cnt,wifi_up_cnt/check_cnt*100,extern_up_cnt,extern_up_cnt/check_cnt*100)
  return title_text + summary_text

def send_message(message):
  send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_ID + '&parse_mode=Markdown&text=' + message
  response = requests.get(send_text)
  return response.json()

if __name__ == "__main__":
  check_network()
  read_csv()
  print_summary()
  send_message(get_daily_summary())