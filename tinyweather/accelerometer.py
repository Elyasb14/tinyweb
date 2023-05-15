import adafruit_msa3xx
import board

class Accelerometer(adafruit_msa3xx.MSA311):
    def __init__(self):
        super().__init__(board.I2C())
    
    def parse_data(self):
        print("%f %f %f" % self.acceleration)