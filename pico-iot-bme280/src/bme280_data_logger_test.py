import machine
import time
from machine import Pin, I2C
import network
import urequests
import json
import gc
import bme280

# Create the Wi-Fi interface in station mode and access the onboard LED
wlan = network.WLAN(network.STA_IF)
board_led = machine.Pin("LED", machine.Pin.OUT)

# Wi-Fi credentials - replace with your own network's SSID and password
ssid = ""
password = ""

# Web app URL for Google Apps Script and time API URL for timestamp retrieval
# Replace with your own URLs - the script URL is the one generated when you deploy your Google Apps Script as a web app, and the time URL is from an online API that returns the current date and time in JSON format
SCRIPT_URL = ""
TIME_URL = ""

# Initialise the BME280 sensor over I2C using GPIO 0 as SDA and GPIO 1 as SCL
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

# Request the current data and time from the online time API
# The timestamp is returned as a string and used when logging readings
def getTime():
    res = urequests.get(url=TIME_URL)
    timestamp = json.loads(res.text)["dateTime"]
    res.close()
    return timestamp

# Connnect the Pico W to Wi-Fi
# The LED is used as a simple connection indicator:
# off while waiting, and on once the connection is made
def connectWifi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected() and wlan.status() >= 0:
            print("Waiting to connect...")
            time.sleep(1)
            board_led.off() 
            
        board_led.on()  
        
        print(wlan.ifconfig())
    else:
        print("Wifi already connected...")
        print(getTime())

# Send the timestamp and temperature value to Google Sheets through Apps Script
# The try-except block here helps prevent the script from stopping if an upload fails
def sendToSpreadsheet(time_value, sensor1):
    try:
        url = f"{SCRIPT_URL}?time={time_value}&sensor1={sensor1}"
        print(url)
        res = urequests.get(url=url)
        res.close()
        gc.collect()
    except Exception:
        print("Upload failed to google sheets")

# Connect to the Wi-Fi network before starting continuous data logging
connectWifi()
wlan.active(True)

# Continuous logging loop:
# gets current timestamp
# reads the BME280 temperature
# format the reading
# upload to Google Sheets
# then it waits 5 seconds before the next reading (needed)
while True:
    timestamp = f"{getTime()}"
    temp = float(bme.values[0][:-1])   
    sensor1 = f"{temp:.2f}"
    sendToSpreadsheet(time_value=timestamp, sensor1=sensor1)
    time.sleep(5)

# Onboard LED is turned off when the script ends
board_led.off()