from flask import Flask, jsonify, render_template, request, send_file, redirect, url_for
from flask_restful import Resource, Api
from tinyweather.env import Rg15, Bme680
#from tinyweather.gps import Gps
import os

bme680 = Bme680()
#rain = Rg15()
#gps = Gps()

app = Flask(__name__)
api = Api(app)

class RawData(Resource):
    def get(self):
        global bme680
        bme680_dict = bme680.parse_data()
        # rain_dict = rain.parse_data()
        return jsonify(bme680_dict)


@app.route('/')
@app.route('/index.html')
def index():
    """Render the index.html template with the title and GPS coordinates."""
    return render_template('index.html', the_title='tinyweather')
                        # , lat=gps.parse_data()["lat"], lon=gps.parse_data()["lon"])

@app.route('/')
@app.route('/data.html')
def data():
    """Render the data.html template with weather and GPS data.

    If the request method is POST, retrieve weather and GPS data and render the template with the data.
    If an exception occurs during data retrieval, render the template with the error message.

    Returns:
        The rendered data.html template.
    """
    bme680_dict = bme680.parse_data()
    rain_dict = rain.parse_data()
    #gps_dict = gps.parse_data()
    return render_template('data.html',
                            temp=bme680_dict["temp (c)"],
                            pressure=bme680_dict["pressure"],
                            humid=bme680_dict["humidity"],
                            gas=bme680_dict["gas"],
                            acc=rain_dict["Acc"],
                            eventacc=rain_dict["EventAcc"],
                            totalacc=rain_dict["TotalAcc"],
 #                           lat=gps_dict["lat"],
  #                          lon=gps_dict["lon"],
   #                         sattelites=gps_dict["num satelites"],
                            the_title="data"
                            )


@app.route('/')
@app.route("/api_info.html")
def api_info():
    """Render the api_info.html template with the title 'api info'."""
    return render_template('api_info.html', the_title='api info')

@app.route('/')
@app.route('/downloads.html')
def downloads():
    """Render the downloads.html template with the list of files in the 'tinyweather/data' directory."""
    files = sorted(os.listdir('tinyweather/data'))
    return render_template('downloads.html', files=files, the_title="downloads")

@app.route('/')
@app.route('/select', methods = ['POST', 'GET'])
def select():
    """Handle the file selection form submission.

    Retrieve the selected file and send it as a response.

    Returns:
        The selected file as a response.
    """
    files = request.form.get('files')
    return send_file(f'tinyweather/data/{files}')

@app.route('/refresh', methods=['POST'])
def refresh():
    # Any necessary processing can be done here
    return redirect(url_for('data'))

api.add_resource(RawData, '/api/raw_data')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
