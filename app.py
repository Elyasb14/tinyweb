from flask import Flask, render_template, request, send_file
import subprocess
app = Flask(__name__)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='tinyweather')


# @app.route('/tinyweather/data')
# def serve_csv():
#     # Replace 'path_to_your_file.csv' with the actual path or URL of your CSV file
#     return send_file('tinyweather/data/03-20-2023-rain.csv', mimetype='text/csv')


@app.route('/', methods=['POST', 'GET'])
@app.route('/data.html')
def data():
    if request.method == 'POST':
        script_output = subprocess.check_output(['python3', 'render_tinyweather_output.py'], universal_newlines=True)
        return render_template('data.html', output=script_output, the_title="data")
    return render_template('data.html', the_title="data")
    

@app.route("/")
@app.route("/README.html")
def README():
    return render_template('README.html', the_title='readme')

@app.route("/")
@app.route("/api_info.html")
def api_info():
    return render_template('api_info.html', the_title='api info')
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
