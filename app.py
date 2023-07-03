from flask import Flask, render_template, request, send_file
from tinyweather.env import Rg15, Bme680
from tinyweather.gps import Gps
import os

bme680 = Bme680()
rain = Rg15("/dev/ttyUSB0")
gps = Gps()

app = Flask(__name__)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', lat=gps.parse_data()["lat"], lon=gps.parse_data()["lon"], the_title='tinyweather')

@app.route('/')
@app.route('/data.html', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        try:
            bme680_dict = bme680.parse_data()
            rain_dict = rain.parse_data()
            gps_dict = gps.parse_data()
            return render_template('data.html', 
                                   temp=bme680_dict["temp (c)"],
                                   pressure=bme680_dict["pressure"],
                                   humid=bme680_dict["hummidity"],
                                   gas=bme680_dict["gas"],
                                   acc=rain_dict["Acc"],
                                   eventacc=rain_dict["EventAcc"],
                                   totalacc=rain_dict["TotalAcc"],
                                   lat=gps_dict["lat"],
                                   lon=gps_dict["lon"],
                                   sattelites=gps_dict["num satelites"],
                                   the_title="data"
                                   )
        except Exception as e:
            return render_template('data.html', output=f"Tinweather not responding, here is the error: {e}",
                                   the_title="data"
                                   )
    return render_template('data.html', the_title="data")
    

@app.route('/')
@app.route("/README.html")
def README():
    return render_template('README.html', the_title='readme')

@app.route('/')
@app.route("/api_info.html")
def api_info():
    return render_template('api_info.html', the_title='api info')


@app.route('/')
@app.route('/downloads.html')
def downloads():
    files = os.listdir('tinyweather/data')
    return render_template('downloads.html', files=files)

@app.route('/')
@app.route('/select', methods = ['POST', 'GET'])
def select():
    files = request.form.get('files')
    return send_file(f'tinyweather/data/{files}')
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)