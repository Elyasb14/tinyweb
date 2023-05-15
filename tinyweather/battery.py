import board
import adafruit_max1704x
import datetime
import pandas as pd
import os

class Battery(adafruit_max1704x.MAX17048):
    def __init__(self) -> None:
        super().__init__(i2c_bus=board.I2C())
    
    def get_timestamp(self) -> dict:
        '''gets timstamp'''
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}

    def parse_data(self): return self.get_timestamp() | {"voltage": self.cell_voltage, "Battery state": self.cell_percent}
    
    def save_data(self, data: dict):
        """saves data to a csv with timestamp"""
        df = pd.DataFrame([data])
        if os.path.isfile(f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-battery.csv"):
            df.to_csv(
                f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-battery.csv", mode="a", header=False, index=False)
            print(
                f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-battery.csv")
            print(df)
        else:
            df.to_csv(
                f"/home/ebianchi/tinyweather/data/{(self.get_timestamp()['date']).replace('/', '-')}-battery.csv", mode="a", index=False)
            print(df)
            
