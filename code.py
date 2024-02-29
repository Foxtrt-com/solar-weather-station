import time
import rtc
import board
import busio
import adafruit_ccs811
from adafruit_bme280 import basic as adafruit_bme280

i2c = board.I2C()  # uses board.SCL and board.SDA

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
ccs811 = adafruit_ccs811.CCS811(i2c)

r = rtc.RTC()

while r.datetime.tm_year != 2000:
    while not ccs811.data_ready:
        pass
    
    timenow = r.datetime
    formatted_time = f"{timenow.tm_mday}/{timenow.tm_mon}/{timenow.tm_year} {timenow.tm_hour}:{timenow.tm_min}:{timenow.tm_sec}"
    
    print("\033[H\033[J", end="")
    print(f"Time: {formatted_time}")
    print("CO2: %0.1f PPM" % ccs811.eco2)
    print("TVOC: %0.1f PPB" % ccs811.tvoc)
    print("Temperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    
    with open("datalog.txt", "a+") as f:
        f.write(f"\n{formatted_time}")
        f.write(f"\nCO2: %0.1f PPM" % ccs811.eco2)
        f.write(f"\nTVOC: %0.1f PPB" % ccs811.tvoc)
        f.write(f"\nTemperature: %0.1f C" % bme280.temperature)
        f.write(f"\nHumidity: %0.1f %%" % bme280.humidity)
        f.write(f"\nPressure: %0.1f hPa\n" % bme280.pressure)

    time.sleep(10*60) # 10 mins
