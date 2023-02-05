from flask import Flask, jsonify, request
import physics_calc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

MIN_TEMPERATURE = 15
MAX_TEMPERATURE = 30
LATITUDE = 30
LONGITUDE = 35
ERROR_CODE = -9
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class SearchResult(db.Model):
    load_mass = db.Column(db.Float, primary_key=True)
    take_off_distance = db.Column(db.Float)
    overweight = db.Column(db.Float)
    take_off_time = db.Column(db.Float)

    def __init__(self, load_mass, take_off_distance, overweight, take_off_time):
        self.load_mass = load_mass
        self.take_off_distance = take_off_distance
        self.overweight = overweight
        self.take_off_time = take_off_time


def requests_weather(url, counter):  # anti server spam handler
    if counter == 8:
        return "error"
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.ConnectionError as e:
        counter += 1
        return requests_weather(url, counter)
    except Exception as g:
        print(f"erorrr ", type(g), g)
        return "problem"


# Flask server
@app.route("/weather", methods=["POST"])
def weather_api_sniffer():  # get the Opearentionable times or temp function
    try:
        year = request.json["year"]
        month = request.json["month"]
        day = request.json["day"]
        print(f"{year}:{month}:{day}")
        url = f'https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={year}-{month}-{day}&end_date={year}-{month}-{day}&hourly=temperature_2m'
        response = requests_weather(url, 1)
        if response.status_code == 200:
            data = response.json()
            relevant_times = []
            if len(data['hourly']['temperature_2m']) == len(data['hourly']['time']):  # if the data is reliable
                for i in range(len(data['hourly']['temperature_2m'])):  # extract all Opearentionable times
                    try:
                        if MIN_TEMPERATURE <= data['hourly']['temperature_2m'][i] <= MAX_TEMPERATURE:
                            relevant_times.append(data['hourly']['time'][i].split("T")[1])
                    except:
                        return "connection _Error"
            print("finish")
            if not relevant_times:  # if there is no times return the temp
                return [data['hourly']['temperature_2m'][1]]
            return relevant_times
        else:
            print('Failed to retrieve data from API')
            return "connection _Error"
    except():
        return "error"
    return "error"


def db_save(result, load_mass):
    if result != ERROR_CODE:
        sr = SearchResult(load_mass, result[1], result[2], result[0])
        db.session.add(sr)
        db.session.commit()
    else:
        print("its wrong!!")


@app.route("/physics_calc", methods=["POST"])
def receive_input():  # main physics calc receive function
    load_mass = request.json["inputData"]
    db_result = SearchResult.query.filter_by(load_mass=load_mass).first()
    if db_result is not None:
        return jsonify(db_result.take_off_time, db_result.take_off_distance,
                       db_result.overweight)
    result = physics_calc.general_calc(int(load_mass))
    db_save(result, load_mass)
    return jsonify(result)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
