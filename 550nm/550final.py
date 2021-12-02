import time
import board
import adafruit_dht
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

analog_in = AnalogIn(board.A1)
dhtDevice = adafruit_dht.DHT11(board.D5)
relay = DigitalInOut(board.D6)
relay.direction = Direction.OUTPUT

def get_voltage(pin):
    return (pin.value * 5) / 65536

relay.value = False
while True:
    soil_moisture = 100-((get_voltage(analog_in)/5)*100)
    print("Soil Moisture= {:.2f} %".format(soil_moisture))
    if soil_moisture >= 0:
        relay.value = False
        print("relay on")
    else:
        relay.value = True
        print("relay on")
        
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)