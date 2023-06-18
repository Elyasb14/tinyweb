import datetime
import os
# import bme280
import board
import adafruit_bme680
import serial
import pandas as pd


# TODO: add turn off command to each of these
i2c=board.I2C()
# rg15 rain gauge class
class Rg15(serial.Serial):
    def __init__(self, dev: str) -> None:
        super().__init__(dev, timeout=3)

    def reset_values(self): self.write(b"o\n")

    def set_mode(self, mode: str): self.write(f"{mode}\n".encode())

    def get_timestamp(self) -> dict:
        '''gets timstamp'''
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

    def get_data(self: serial.Serial) -> str:
        """reads data from rain gauge returns data as a string"""
        self.write(b"r\n")
        return self.readline().decode().strip("\r\n")

    def parse_data(self) -> dict:
        '''returns list of keys and values'''
        groups = [group.strip().split(" ") for group in (' '.join(self.get_data().split())).split(",")]
        try:
            values = [group[1] for group in groups]
            keys = [group[0] for group in groups]
            return self.get_timestamp() | {value[0]: value[1] for value in zip(keys, values)}
        except IndexError:
            print("invalid response from device")
            return self.get_timestamp()
        except ValueError:
            print("invalid response from device")
            return self.get_timestamp()
    def save_data(self, data: list) -> dict:
        """saves data to a csv with timestamp"""
        df = pd.DataFrame([data])
        if os.path.isfile(f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv"):
            df.to_csv(f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv", header=False, mode="a", index=False)
            print(f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-rain.csv")
            print(df)
        else:
            print("debug")
            df.to_csv(
                f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv", mode="a", index=False)
            print(df)
            

# # BME280 sensor class
# class Bme280(bme280.BME280):
#     def __init__(self) -> None:
#         super().__init__()
        
#     def get_timestamp(self) -> dict:
#         '''gets timstamp'''
#         x = datetime.datetime.now()
#         keys = ["date", "time"]
#         return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

#     def parse_data(self): return self.get_timestamp() | {"temp (c)": self.get_temperature(), "pressure": self.get_pressure(), "hummidity": self.get_humidity()}

#     def save_data(self, data: dict) -> dict:
#         """saves data to a csv with timestamp"""
#         df = pd.DataFrame([data])
#         if os.path.isfile(f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme280.csv"):
#             df.to_csv(
#                 f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme280.csv", mode="a", header=False, index=False)
#             print(
#                 f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-bme280.csv")
#             print(df)

#         else:
#             df.to_csv(
#                 f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme280.csv", mode="a", index=False)
#             print(df)
            

class Bme680(adafruit_bme680.Adafruit_BME680_I2C):
    def __init__(self) -> None:
        super().__init__(i2c)
    
    def get_timestamp(self) -> dict:
        '''gets timstamp'''
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

    def parse_data(self): return (self.get_timestamp() | {"temp (c)": self.temperature, "pressure": self.pressure, "hummidity": self.humidity, "gas": self.gas})
    
    def save_data(self, data: dict):
        """saves data to a csv with timestamp"""
        df = pd.DataFrame([data])
        if os.path.isfile(f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv"):
            df.to_csv(
                f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv", mode="a", header=False, index=False)
            print(
                f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv")
            print(df)
        else:
            print("debug")
            df.to_csv(
                f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv", mode="a", index=False)
            print(df)
