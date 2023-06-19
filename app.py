from flask import Flask, render_template, request, send_file
import subprocess
from tinyweather.env import Rg15, Bme680
from tinyweather.gps import Gps

bme680 = Bme680()
rain = Rg15("/dev/ttyUSB0")
gps = Gps()

app = Flask(__name__)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='tinyweather')

@app.route('/', methods=['POST', 'GET'])
@app.route('/data.html')
def data():
    if request.method == 'POST':
        try:
            # script_output = subprocess.check_output(['python3', 'tinyweather/output.py'], universal_newlines=True)
            bme680_dict = bme680.parse_data()
            rain_dict = rain.parse_data()
            gps_dict = gps.parse_data()
            return render_template('data.html', 
                                   bme680_dict=bme680_dict, 
                                   rain_dict=rain_dict, 
                                   gps_dict=gps_dict,
                                   the_title="data"
                                   )
        except Exception as e:
            return render_template('data.html', output=f"Tinweather not responding, here is the error: {e}",
                                   the_title="data"
                                   )
    return render_template('data.html', the_title="data")
    

@app.route("/")
@app.route("/README.html")
def README():
    return render_template('README.html', the_title='readme')

@app.route("/")
@app.route("/api_info.html")
def api_info():
    return render_template('api_info.html', the_title='api info')

@app.route("/", methods=["GET", "REQUEST"])
@app.route("/<string:file>/")
def download_file(file): return send_file(f"tinyweather/data/{file}.csv")
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
