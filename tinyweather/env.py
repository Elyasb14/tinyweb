import datetime
import os
import board
import adafruit_bme680
import serial
import pandas as pd
from pathlib import Path



i2c=board.I2C()
# rg15 rain gauge class
class Rg15(serial.Serial):
    def __init__(self, dev: str = '/dev/ttyUSB0') -> None:
        super().__init__(dev, timeout=3)

    def reset_values(self): self.write(b"o\n")

    def set_mode(self, mode: str): 
        """Set the mode of the rain gauge.

        Args:
            mode: The mode to set for the rain gauge.
        """
        self.write(f"{mode}\n".encode())

    def get_timestamp(self) -> dict:
        """Get the current timestamp.

        Returns:
            A dictionary containing the date and time.
        """
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

    def get_data(self) -> str:
        """reads data from rain gauge returns data as a string"""
        self.write(b"r\n")
        return self.readline().decode().strip("\r\n")

    def parse_data(self) -> dict:
        """Parse the data from the rain gauge.

        Returns:
            A dictionary of keys and values representing the parsed data.
        """
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
        """Save data to a CSV file with a timestamp.

        Args:
            data: The data to be saved.

        Returns:
            A dictionary representing the saved data.
        """
        df = pd.DataFrame([data])
        path = Path(__file__).parent / 'data'
        if os.path.isfile(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv"):
            df.to_csv(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv", 
                      header=False, mode="a", index=False)
            print(f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-rain.csv")
            print(df)
        else:
            df.to_csv(
                path / f"{(self.get_timestamp()['date']).replace('/', '-')}-rain.csv", mode="a", index=False)
            print(df)
            
            

class Bme680(adafruit_bme680.Adafruit_BME680_I2C):
    def __init__(self) -> None:
        super().__init__(i2c)
    
    def get_timestamp(self) -> dict:
        """Get the current timestamp.

        Returns:
            A dictionary containing the date and time.
        """
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

    def parse_data(self) -> dict:
        """Parse the data from the BME680 sensor.

        Returns:
            A dictionary containing the parsed data including temperature, pressure, humidity, and gas.
        """
        self.temperature
        return (self.get_timestamp() | {"temp (c)": self.temperature, "pressure": self.pressure, "humidity": self.humidity, "gas": self.gas})
    
    def save_data(self, data: dict):
        """Save data to a CSV file with a timestamp.

        Args:
            data: The data to be saved as a dictionary.

        Returns:
            None
        """
        df = pd.DataFrame([data])
        path = Path(__file__).parent / 'data'
        if os.path.isfile(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv"):
            df.to_csv(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv", mode="a", header=False, index=False)
            print(f"Saved to {(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv")
            print(df)
        else:
            df.to_csv(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv", mode="a", index=False)
            print(df)
