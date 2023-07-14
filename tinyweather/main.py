from env import Rg15, Bme680
from gps import Gps
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--env", help="enable environmental sensor", action=Bme680().save_data(Bme680().parse_data()))
parser.add_argument("--rain", help="enable rain gauge", action=Rg15().save_data(Rg15().parse_data()))
parser.add_argument("--gps", help="enable gps", action=Gps().save_data(Gps().parse_data()))
args = parser.parse_args()