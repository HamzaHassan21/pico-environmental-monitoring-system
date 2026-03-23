from machine import Pin, I2C
import bme280
from time import sleep

# Initialise I2C communication and configure the BME280 sensor
# GPIO 0 is used for SDA and GPIO 1 for SCL
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

# Configuring the onboard LED as a visual indicator
# The LED remains on while the script is collecting sensor data
led = Pin("LED", Pin.OUT)

led.on()

# variables for averaging - temperature, pressure, humidity
total_temp = 0
total_pressure = 0
total_humidity = 0

# 5 consecutive readings from the BME280 sensor, can verify through shell
for i in range(5):
    temp = float(bme.values[0][:-1]) # removing c and converting to float
    pressure = float(bme.values[1][:-3]) # removing hPa and converting to float
    humidity = float(bme.values[2][:-1]) # removing % and convert to float

    print(f"Reading {i+1}: T={temp}C  H={humidity}%  P={pressure}hPa")

    # Add values to totals for averaging
    total_temp += temp
    total_pressure += pressure
    total_humidity += humidity

    sleep(1) # one second pause between each sensor reading reducing noise and cpu usage

# Calculating the temperature, humidity, and pressure values and prints them out.
avg_temp = total_temp / 5
avg_pressure = total_pressure / 5
avg_humidity = total_humidity / 5

print("\nAverages:")
print(f"Temperature: {avg_temp:.2f} C")
print(f"Humidity: {avg_humidity:.2f} %")
print(f"Pressure: {avg_pressure:.2f} hPa")

# lastly LED is turned off to indicate the script has finished running (Script has been executed)
led.off()