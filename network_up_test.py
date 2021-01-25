import os
import time
from datetime import datetime

hostname = "google.com"
filename = "demofile.txt"
separator = ","
up_cnt = 0
down_cnt = 0

def ping():
    return os.system("ping -c 1 " + hostname)

def check_network():
  file = open(filename,"a")
  file.write(str(datetime.now()) + separator)
  if ping() == 0:
    file.write("up\n")
    file.close()
    return True
  else:
    file.write("down\n")
    file.close()
    return False

def print_summary():
  file = open(filename,"a")
  file.write("------------------------\nUp: " + str(up_cnt) + "\nDown: " + str(down_cnt) + "\n")
  file.close()

if __name__ == "__main__":
  for i in range(0,5):
    if True == check_network():
      up_cnt += 1
    else: 
      down_cnt += 1
    time.sleep(1)
  print_summary()