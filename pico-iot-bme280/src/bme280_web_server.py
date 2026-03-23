import machine
from machine import Pin, I2C
from time import sleep
import network
import socket
import bme280

# Wi-Fi Credentials - replace with your own network's SSID and password
ssid = ""
password = ""

# Initialise the BME280 sensor over I2C
# The BME280 communicates over I2C, initialise the I2C
# using GPIO 0 (SDA) and GPIO 1 (SCL), then create a BME280 object
# The sensor provides temperature, pressure, and humidity readings
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

# Connect the Pico W to the Wi-Fi network
# The function activates the wireless interface and waits until a connection is established
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        print("Waiting for connection ...")
        sleep(1)

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Open a socket on port 80 so that the Pico W can act as a simple web server
# Devices on the same local network can access the webpage using the Pico W IP address
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

# HTML webpage template (simple HTML)
# The page refreshes automatically every 5 seconds to show updated sensor values
def webpage(reading):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>BME280 Sensor Readings</title>
        <meta http-equiv="refresh" content="5"> 
        </head>
        <body>
        <h2>BME280 Live Readings</h2>
        <p>{reading}</p>
        </body>
        </html>
        """
    return str(html)

# Main web server loop
# Function waits for incoming requests, each time a client connects the Pico reads fresh sensor values.
def serve(connection):
    while True: 
        client = connection.accept()[0]  # Accepting incoming browser connection
        request = client.recv(1024)      # Receive HTTP request
        request = str(request)

        # reading live sensor values from the BME280
        temperature = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
        
        # Format the reading for display on page
        reading = f"Temperature: {temperature} | Pressure: {pressure} | Humidity: {humidity}"
        html = webpage(reading)

        # Send the webpage to the client
        client.send(html)
        client.close()

# Program Entry Point, attempts to connect to Wi-Fi, start the web server and serving live sensor data
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    # if user stops the script manually, resets the Pico W safely
    machine.reset()