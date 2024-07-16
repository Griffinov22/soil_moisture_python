from gpiozero import MCP3008
from time import sleep
from functools import reduce
from garden_email import send_email
from dotenv import load_dotenv
import os
config = load_dotenv(".env")

# FROM TESTING: HIGHEST (DRYEST VALUE) 704 || LOWEST (WETTEST VALUE) 345

am = MCP3008(channel=0,clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=5)


COUNT = 15
TEMP_ARR = []
notification_list = os.getenv('EMAIL_LIST').split(",")


# TESTING
# while True:
#   print("soil moisture level: %s" % am.raw_value)
#   sleep(0.5)

def get_temps(count):
  for i in range(count):
    moisture_value = am.raw_value
    TEMP_ARR.append(moisture_value)
    sleep(1)


# MAIN
get_temps(COUNT)
testAvg = round((reduce(lambda a,b: a+b, TEMP_ARR)/ COUNT), 2)
# if average is really low or really high, run test to be sure
if (testAvg < 400 or testAvg > 650):
  testAvg = testAvg = round((reduce(lambda a,b: a+b, TEMP_ARR)/ COUNT), 2)
# notify me via email
send_email(testAvg, receiving_emails=notification_list)

