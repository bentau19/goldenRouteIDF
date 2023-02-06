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



# Function to handle weather request with anti-spam mechanism
def requests_weather(url, counter=1):
    # Return "error" if maximum retry attempts reached
    if counter == 8:
        return "error"

    try:
        # Make API request and add timeout value with retry counter
        response = requests.get(url, timeout=(0.25 + (counter * 0.25)))
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        # Retry request on connection or read timeout error
        return requests_weather(url, counter + 1)
    except Exception as g:
        return "problem"

# Flask route to handle weather API request
@app.route("/weather", methods=["POST"])
def weather_api_sniffer():
    try:
        # Get year, month and day from POST request
        year = request.json["year"]
        month = request.json["month"]
        day = request.json["day"]
        # Form URL for API request
        url = f'https://archive-api.open-meteo.com/v1/archive?latitude={LATITUDE}&longitude={LONGITUDE}&start_date={year}-{month}-{day}&end_date={year}-{month}-{day}&hourly=temperature_2m'

        # Call function to make API request
        response = requests_weather(url)
        if type(response) == str:
            # Return "connection error" if request fails
            return "connection error"
        if response.status_code == 200:
            data = response.json()
            relevant_times = []
            # Check if both temperature and time data exists for each hour
            if len(data['hourly']['temperature_2m']) == len(data['hourly']['time']):
                for i in range(len(data['hourly']['temperature_2m'])):
                    # Append relevant time if temperature is within specified range
                    if MIN_TEMPERATURE <= data['hourly']['temperature_2m'][i] <= MAX_TEMPERATURE:
                        relevant_times.append(data['hourly']['time'][i].split("T")[1])
            # Return first temperature if no relevant times found
            if not relevant_times:
                return [data['hourly']['temperature_2m'][1]]
            return relevant_times
        else:
            # Return "connection error" if API request fails
            return "connection error"
    except:
        # Return "error" for all other exceptions
        return "error"


def db_save(result, load_mass):
    # function to save results to database

    # check if result is not equal to error code
    if result != ERROR_CODE:
        # create a SearchResult object with load_mass, take_off_time, take_off_distance, and overweight
        sr = SearchResult(load_mass, result[1], result[2], result[0])
        # add the object to the database session
        db.session.add(sr)
        # commit the session to save the changes
        db.session.commit()
    else:
        # if result is equal to error code, print error message
        print("its wrong!!")


@app.route("/physics_calc", methods=["POST"])
def receive_input():
    # main physics calculation receive function

    # get the load_mass from the request JSON
    load_mass = request.json["inputData"]
    # search for existing result in the database
    db_result = SearchResult.query.filter_by(load_mass=load_mass).first()
    # if result is found in the database
    if db_result is not None:
        # return the take_off_time, take_off_distance, and overweight
        return jsonify(db_result.take_off_time, db_result.take_off_distance,
                       db_result.overweight)
    # if result is not found in the database
    result = physics_calc.general_calc(int(load_mass))
    # save the result to the database
    db_save(result, load_mass)
    # return the result
    return jsonify(result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
