import os
import csv
from datetime import datetime

dt = datetime.now()
hostname_gateway = "fritz.box"
hostname_wifi = ""
hostname_extern = "google.com"
filename = "network_test_%04i%02i%02i.csv" % (dt.year,dt.month,dt.day) 
gateway_up_cnt = 0
wifi_up_cnt = 0
extern_up_cnt = 0
check_cnt = 0

def ping(hostname):
    return os.system("ping -c 1 " + hostname)

def print_summary():
  print("Gateway: " + str(gateway_up_cnt) + " (" + str(gateway_up_cnt/check_cnt*100) + "%)")
  print("Wifi: " + str(wifi_up_cnt) + " (" + str(wifi_up_cnt/check_cnt*100) + "%)")
  print("Extern: " + str(extern_up_cnt) + " (" + str(extern_up_cnt/check_cnt*100) + "%)")

if __name__ == "__main__":
  with open(filename,"a") as csvfile:
    csv_writer = csv.writer(csvfile)

    if os.stat(filename).st_size == 0:
      csv_writer.writerow(['date','gateway','wifi','extern'])
    
    gateway_check = False
    wifi_check = False
    extern_check = False
    if ping(hostname_gateway) == 0:
      gateway_check = True
      gateway_up_cnt += 1
    if ping(hostname_wifi) == 0:
      wifi_check = True
      wifi_up_cnt += 1
    if ping(hostname_extern) == 0:
      extern_check = True
      extern_up_cnt += 1

      csv_writer.writerow(["%02i:%02i:%02i" % (dt.hour,dt.minute,dt.second),gateway_check,wifi_check,extern_check])
      check_cnt += 1
  print_summary()