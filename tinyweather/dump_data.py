from env import Rg15, Bme680
import argparse
import psutil

pid = psutil.Process()
# adds cli flags
parser = argparse.ArgumentParser()
parser.add_argument("--device", default="/dev/ttyUSB0", help="serial device to use")
parser.add_argument("--reset", type=bool, help="reset all sensors that have the ability to be reset")

args = parser.parse_args()

rain = Rg15(args.device)
env = Bme680()
memory_usage = pid.memory_info().rss
memory_usage_mb = memory_usage / 1024 / 1024


if args.reset:
    # rain.reset_values()
    pass
else:
    print(rain.parse_data())
    print(env.parse_data())
    # rain.save_data(rain.parse_data())
    # env.save_data(env.parse_data())
    print(f"Memory usage: {memory_usage_mb:.2f} MB")

