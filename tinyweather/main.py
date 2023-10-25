from env import Rg15, Bme680

    
env = Bme680()
rain = Rg15()

env.save_data(env.parse_data())
rain.save_data(rain.parse_data())
