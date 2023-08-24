from flask_restful import Resource, output_json
from tinyweather.env import Rg15, Bme680

bme680 = Bme680()
rain = Rg15()

class RawData(Resource):
    def get(self):
        bme680_dict = bme680.parse_data()
        rain_dict = rain.parse_data()
        return output_json(bme680_dict | rain_dict)
    
class Rain(Resource):
    def get(self):
        rain_dict = rain.parse_data()
        return output_json(rain_dict)
        
class Env(Resource):
    def get(self):
        bme680_dict = bme680.parse_data()
        return output_json(bme680_dict)