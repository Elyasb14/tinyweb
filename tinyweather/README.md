# ***tinyweather***

Tinyweather is a python library for interfacing with environmental sensors and analyzing the data received. Right now we support the [RG-15 rain gauge](https://rainsensors.com/products/rg-15/), the [Bosch BME280](https://shop.pimoroni.com/en-us/products/bme280-breakout), the [Bosch BME680](https://www.adafruit.com/product/3660?gclid=CjwKCAjw0N6hBhAUEiwAXab-TYMXNG9DUUJA3Fm7TbSlkqZ6VzyJjTGJsNlhUxS3C3BAgEiLLg399xoCRQcQAvD_BwE), the [Bosch BME688](https://www.adafruit.com/product/5046), and other state of health monitoring devices, we will support many more in the future. Tinyweather is sort of inspired by the following [library](https://github.com/waggle-sensor), but aims to be slimmed down and simplified, making it easy to add new sensors and features. This library was developed using a [raspberry pi model 4b](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), but any single board computer with GPIO should work. Tinyweather is the future of remote environmental monitoring.

## ***Release Installation***

```bash
pip install tinyweather
```

## ***Quicker Release Installation***

```bash
git clone https://github.com/Elyasb14/tinyweather.git
cd tinyweather
python3 -m pip install .
```

## ***Example Usage***

```python
from tinyweather import sensors

rain = sensors.Rg15("/dev/ttyUSB0")
env = sensors.Bme280()

print(rain.parse_data())
print(env.parse_data())
```

## ***Data Collection***

Create a python file with the following code to save sensor data to the files `<date>-rain.csv` and `<date>-bme280.csv`

```python
from tinyweather import sensors
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--device", default="/dev/ttyUSB0", help="serial device to use")
parser.add_argument("--reset", type=bool, help="reset all sensors that have the ability to be reset")

args = parser.parse_args()

rain = sensors.Rg15(args.device)
env = sensors.Bme280()
env.parse_data()

def main():
    rain.save_data(rain.parse_data())
    env.save_data(env.parse_data())
main()
```

## ***Supported Sensors***

- [RG-15 rain gauge](https://rainsensors.com/products/rg-15/)
- [Bosch BME280](https://shop.pimoroni.com/en-us/products/bme280-breakout) 
- [Bosch BME680](https://www.adafruit.com/product/3660?gclid=CjwKCAjw0N6hBhAUEiwAXab-TYMXNG9DUUJA3Fm7TbSlkqZ6VzyJjTGJsNlhUxS3C3BAgEiLLg399xoCRQcQAvD_BwE)
- [Bosch BME688](https://www.adafruit.com/product/5046)

## ***Extra***

Extra is a directory for small weather applications whether it be swe or rainfall plotting.

## ***Tests***

