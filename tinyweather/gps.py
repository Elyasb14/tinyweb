import datetime
from typing import Any
import board
import adafruit_gps


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
    

        
