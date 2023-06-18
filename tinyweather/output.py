from env import Rg15, Bme680

rain = Rg15("/dev/ttyUSB0")
env = Bme680()

env_dict = env.parse_data()
rain_dict = rain.parse_data()

print("environmental data")
for key, val in env_dict.items():
    print(key, val)

print("\n")

print("rainfall")
for key, val in rain_dict.items():
    print(key, val)
