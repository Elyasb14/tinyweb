import datetime
import board
import adafruit_gps
import pandas as pd
import os
from pathlib import Path

class Gps(adafruit_gps.GPS_GtopI2C):
    def __init__(self) -> None:
        """Initialize the GPS class."""
        super().__init__(i2c_bus=board.I2C())
    
    def get_timestamp(self) -> dict:
        """Get the current timestamp.

        Returns:
            A dictionary containing the date and time.
        """
        x = datetime.datetime.now()
        keys = ["date", "time"]
        return {value[0]: value[1] for value in zip(keys, x.strftime("%m/%d/%Y, %H:%M:%S").replace(",", "").split(" "))}
    
    def turn_off(self) -> None:
        """Turn off the GPS module."""
        self.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    
    def parse_data(self) -> dict:
        """Parse the data from the GPS module.

        Returns:
            A dictionary containing the parsed GPS data including latitude, longitude, altitude, and number of satellites.
        """
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
                                               "num satellites": self.satellites}
    
    def save_data(self, data: dict):
        """Save data to a CSV file with a timestamp.

        Args:
            data: The data to be saved as a dictionary.

        Returns:
            None
        """
        df = pd.DataFrame([data])
        path = Path(__file__).parent / 'data'
        if os.path.isfile(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv"):
            df.to_csv(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv", mode="a", header=False, index=False)
            print(f"Saved to {(self.get_timestamp()['date']).replace('/', '-')}-gps.csv")
            print(df)
        else:
            print("Debug")
            df.to_csv(path / f"{(self.get_timestamp()['date']).replace('/', '-')}-gps.csv", mode="a", index=False)
            print(df)
        

if __name__ == "__main__":
    gps = Gps()
    print(gps.parse_data())
