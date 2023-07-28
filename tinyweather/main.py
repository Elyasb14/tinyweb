from env import Rg15, Bme680
from gps import Gps

    

env = Bme680()
rain = Rg15()
gps = Gps()

env.save_data(env.parse_data())
rain.save_data(rain.parse_data())
gps.save_data(gps.parse_data())