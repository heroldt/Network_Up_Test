import os
import time
import csv
from datetime import datetime

hostname_gateway = "fritz.box"
hostname_wifi = ""
hostname_extern = "google.com"
filename = "test1.csv"
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
  with open(filename,"w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['date','gateway','wifi','extern'])
    
    for i in range(0,5):
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

      csv_writer.writerow([datetime.now(),gateway_check,wifi_check,extern_check])
      check_cnt += 1
      time.sleep(60)
  print_summary()