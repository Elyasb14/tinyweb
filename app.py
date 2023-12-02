
from flask import Flask, render_template, request, send_file, redirect, url_for
from tinyweather.env import Rg15, Bme680
from flask_restful import Api
from api import RawData, Env, Rain
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge

bme680 = Bme680()
rain = Rg15()

app = Flask(__name__)
api = Api(app)

METRICS = {
    "temperature": Gauge(
        "temperature", "temperature"
    ),
}

def env_metric(): 
    bme_680_dict = bme680.parse_data()
    temp = float(bme_680_dict["temp (c)"])
    METRICS["temperature"].set(temp)

env_metric()

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='tinyweather')

@app.route('/')
@app.route('/data.html')
def data():
    bme680_dict = bme680.parse_data()
    rain_dict = rain.parse_data()
    return render_template('data.html',
                            temp=bme680_dict["temp (c)"],
                            pressure=bme680_dict["pressure"],
                            humid=bme680_dict["humidity"],
                            gas=bme680_dict["gas"],
                            acc=rain_dict["Acc"],
                            eventacc=rain_dict["EventAcc"],
                            totalacc=rain_dict["TotalAcc"],
                            the_title="data"
                            )


@app.route('/')
@app.route("/api_info.html")
def api_info():
    return render_template('api_info.html', the_title='api info')

@app.route('/')
@app.route('/downloads.html')
def downloads():
    files = sorted(os.listdir('tinyweather/data'))
    return render_template('downloads.html', files=files, the_title="downloads")

@app.route('/')
@app.route('/select', methods = ['POST', 'GET'])
def select():
    files = request.form.get('files')
    return send_file(f'tinyweather/data/{files}')

@app.route('/refresh', methods=['POST'])
def refresh():
    return redirect(url_for('data'))

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


api.add_resource(RawData, '/raw_data')
api.add_resource(Env, '/env')
api.add_resource(Rain, '/rain')


if __name__ == '__main__':
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
    })
    app.run(debug=True, host="0.0.0.0", port=5001)
