# ***tinyweather***

create a main.py file and add the following code to it

```python
from env import Rg15, Bme680
from gps import Gps

# initialize sensors
env = Bme680()
rain = Rg15()
gps = Gps()

# save parsed data from sensors in tinyweather/data
env.save_data(env.parse_data())
rain.save_data(rain.parse_data())
gps.save_data(gps.parse_data())
```

when you run **cron.sh** from the root directory of tinyweb, this program will automatically save data to a csv every 300 seconds, with a new csv being created daily. you can change this frequency by modifying the **cron.sh** file.
