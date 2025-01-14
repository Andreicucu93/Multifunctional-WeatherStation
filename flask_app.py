from flask import Flask
from pathlib import Path
from weather import generate_weather_report

file_path = Path(__file__).parent / 'log_prompts.txt'



#discontinued method of grabbing data from LogFile(txt) - still active
#def get_content():
#    with open(file_path, 'r') as logfile:
#        content = logfile.readlines()
#        return '<br>'.join(line.strip() for line in content)


app = Flask(__name__)

@app.route('/')
def bucharest_weather():
    weather_data = generate_weather_report()
    #content = get_content() #Part of discontinued method - still active
    return f'''
    <html>
        <head>
	        <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Bucharest - soviet weather</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
            <meta http-equiv="refresh" content="3600">
        </head>

        <body><center>

        <p style="font-size: 20px;"> <H1><strong style="color: red;">Вучаrest weather bulletin</strong></H1> <p>
        <p><img src="{{url_for('static', filename='header.png')}}"></p>

                    <strong>2023 Temperature:</strong> {weather_data['previous_temp']}°C<br>
                    <strong>Live Temperature:</strong> {weather_data['current_temp']}°C<br>
                    <strong>Temperature Difference:</strong> {weather_data['difference_in_temperature']}°C<br>
                    <strong>Update Time:</strong> {weather_data['converted_time']} on {weather_data['converted_date']}<br><br>
                    <em>{weather_data['chat_conclusion']}</em>
        </center></body>
    </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)
