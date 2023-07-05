import datetime
import board
import adafruit_gps
import pandas as pd
import os
from pathlib import Path

class Gps(adafruit_gps.GPS_GtopI2C):
    def __init__(self) -> None:
        super().__init__(i2c_bus=board.I2C())
        
    
    def get_timestamp(self) -> dict:
        '''gets timstamp'''
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}
    
    def turn_off(self) -> None: self.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    
    def parse_data(self) -> dict:
        while True:
            self.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            self.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
            self.send_command(b"PMTK220,1000")
            self.update()
            if not self.has_fix:
                continue
            else:
                return self.get_timestamp() | {"lat": self.latitude, 
                                               "lon": self.longitude, 
                                               "altitude": self.altitude_m,
                                               "num satelites": self.satellites}
    
    
    def save_data(self, data: dict):
            """saves data to a csv with timestamp"""
            df = pd.DataFrame([data])
            path = Path(__file__).parent / 'data'
            if os.path.isfile(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv"):
                df.to_csv(
                    path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv", 
                    mode="a", 
                    header=False, 
                    index=False
                )
                print(
                    f"saved to {(self.get_timestamp()['date']).replace('/', '-')}-bme680.csv")
                print(df)
            else:
                print("debug")
                df.to_csv(
                    path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv", mode="a", index=False)
                print(df)
        

if __name__ == "__main__":
    gps = Gps()
    print(gps.parse_data())
