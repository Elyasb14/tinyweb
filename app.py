from flask import Flask, render_template, request, send_file
from tinyweather.env import Rg15, Bme680
from tinyweather.gps import Gps
import os

bme680 = Bme680()
rain = Rg15("/dev/ttyUSB0")
gps = Gps()

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    """Render the index.html template with the title and GPS coordinates."""
    return render_template('index.html', the_title='tinyweather', lat=gps.parse_data()["lat"], lon=gps.parse_data()["lon"])

@app.route('/')
@app.route('/data.html', methods=['POST', 'GET'])
def data():
    """Render the data.html template with weather and GPS data.

    If the request method is POST, retrieve weather and GPS data and render the template with the data.
    If an exception occurs during data retrieval, render the template with the error message.

    Returns:
        The rendered data.html template.
    """
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
    """Render the README.html template with the title 'readme'."""
    return render_template('README.html', the_title='readme')

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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
