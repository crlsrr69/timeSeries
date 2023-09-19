from flask import Flask, request, jsonify
import requests
import pandas as pd
from datetime import date, timedelta

app = Flask(__name__)

apiKey = 'ac45318b3ed78a56609523496d001c4b'
cityName = 'Angeles City'
countryCode = 'PH'

@app.route('/weather', methods=['GET'])
def get_weather_data():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    weather_df = fetch_weather_data(start_date, end_date)

    if weather_df is None:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    weather_json = weather_df.to_dict(orient='records')

    return jsonify(weather_json)

def fetch_weather_data(start_date, end_date):
    weather_df = pd.DataFrame(columns=['Date', 'Temperature (Celsius)'])

    current_date = start_date

    while current_date <= end_date:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=ac45318b3ed78a56609523496d001c4b'

        try:
            response = requests.get(url)

            response.raise_for_status()

            weather_data = response.json()
            temperature_kelvin = weather_data.get('main', {}).get('temp')

            if temperature_kelvin is not None:
                temperature_celsius = temperature_kelvin - 273.15

                weather_df = weather_df.append({'Date': current_date, 'Temperature (Celsius)': temperature_celsius},
                                               ignore_index=True)
        except requests.exceptions.RequestException as e:

            print(f'Error: {e}')
            return None

        current_date += timedelta(days=1)

    return weather_df

if __name__ == '__main__':
    app.run(debug=True)
