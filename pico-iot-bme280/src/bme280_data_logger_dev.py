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

# Request the current timestamp from the online time API
# The try-except block prevents the program from stopping if the API request fails
def getTime():
    try:
        res = urequests.get(url=TIME_URL)
        timestamp = json.loads(res.text)["dateTime"]
        res.close()
        return timestamp
    except:
        print("Time API error")
        return "Time unavailable"

# Connect the Pico W to the Wi-Fi network
# The onboard LED acts as a simple indicator during connection
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

# Send timestamp, temperature, pressure, and humidity to Google Sheets
# The try-except block prevents failed uploads from crashing the script
def sendToSpreadsheet(time_value, temp, pressure, humidity):
    try:
        url = "{}?time={}&temp={}&pressure={}&humidity={}".format(
            SCRIPT_URL, time_value, temp, pressure, humidity
        )
        print(url)
        res = urequests.get(url=url)
        print(res.text)
        res.close()
        gc.collect()
    except:
        print("Error uploading data...")

# Connect to the Wi-Fi network before starting the logging process
connectWifi()
wlan.active(True)

# Collect and upload 20 BME280 sensor readings at 5‑second intervals
for i in range(20):
    timestamp = "{}".format(getTime())

    # Extract numeric values from the BME280 output strings
    temp = float(bme.values[0][:-1])
    pressure = float(bme.values[1][:-3])
    humidity = float(bme.values[2][:-1])
 
    # Format values to two decimal places for cleaner logging
    temp_value = "{:.2f}".format(temp)
    pressure_value = "{:.2f}".format(pressure)
    humidity_value = "{:.2f}".format(humidity)

    # Print reading to shell for verification
    print("Reading {}".format(i + 1))
    print("{} | Temperature: {}C | Pressure: {}hPa | Humidity: {}%".format(
        timestamp, temp_value, pressure_value, humidity_value
    ))

    # Upload the reading to Google Sheets
    sendToSpreadsheet(
        time_value=timestamp,
        temp=temp_value,
        pressure=pressure_value,
        humidity=humidity_value
    )

    time.sleep(5) # Wait before taking the next reading (needed)

# Turn off LED when script completes
board_led.off()