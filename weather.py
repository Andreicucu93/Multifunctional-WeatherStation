from datetime import datetime
import requests, os
from pytz import timezone
import pandas as pd
from openai import OpenAI
from manage_database import load_database
from pathlib import Path
import random
from ai_profiles import profiles


def generate_prompt(current_temp, previous_temp, difference_in_temperature):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"{profiles['com_sys_role'][0]}"},
            {"role": "user",
             "content": f"Current temp:{current_temp}°C; 1 year ago temp:{previous_temp}°C. Keywords: {load_database(party='communism')}{profiles['com_sys_role'][1]}"}
        ],
        max_tokens=180)
    chat_conclusion = completion.choices[0].message.content
    with open('cached_prompts.txt', 'a', encoding='utf-8') as promptfile:
        promptfile.write(chat_conclusion + '\n')
    return chat_conclusion


def check_cache(current_temp, previous_temp, difference_in_temperature):
    if not os.path.exists('cached_prompts.txt'):
        open('cached_prompts.txt', 'w').close()

    with open('cached_prompts.txt', 'r') as promptfile:
        rows = promptfile.readlines()

    if len(rows) < 5:
        print('New prompt generated.')
        return generate_prompt(current_temp, previous_temp, difference_in_temperature)
    else:
        print('Stock prompt recirculated.')
        return random.choice(rows).strip()

def generate_weather_report():
    #Selecting 2023 data (day, hour, temp)
    csv_file_path = Path(__file__).parent / 'bucharest 2023-08-15 to 2023-12-31.csv'
    data = pd.read_csv(csv_file_path)
    hourly_ds_2023 = data['datetime']
    bucharest_timezone = timezone('Europe/Bucharest')
    converted_time = (datetime.now(bucharest_timezone).strftime('%H:%M'))
    converted_date = (datetime.now(bucharest_timezone).strftime('%d-%m-%Y'))

    time_now = ((datetime.now(bucharest_timezone).strftime('%H')) + ':00')
    def calculate_previous_temp():
        for time in hourly_ds_2023:
            current_date_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            current_time = current_date_time.strftime("%H:%M")

            if current_time == time_now:
                return data.loc[data['datetime'] == time, 'temp'].values[0]
        return None

    previous_temp = calculate_previous_temp()
    #END Selecting 2023 data


    #Current data
    url = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"
    response = requests.get(url)
    data = response.json()

    current_temp = None
    for features in data['features']:
        if features['properties']['nume'] == 'BUCURESTI FILARET':
            current_temp = float(features['properties']['tempe'])
    #END Current data

    difference_in_temperature = round(float(current_temp - previous_temp), 2)

    chat_conclusion = check_cache(current_temp, previous_temp, difference_in_temperature)

    data_log = f'''
    2023 temp: {previous_temp}°C
    Live temp: {current_temp}°C
    Difference: {round(float(current_temp - previous_temp), 2)}°C
    @update time {str(converted_time)} {converted_date}
    {chat_conclusion}
    '''

    def write_log():
        with open('log_prompts.txt', 'w', encoding='utf-8') as newlogfile:
            newlogfile.write(f'{data_log}')
            newlogfile.close()
        with open('log_archive.txt', 'a', encoding='utf-8') as logarchive:
            logarchive.write(f'{data_log}\n\n')

    write_log()

    print(data_log)
    return {
        "previous_temp": previous_temp,
        "current_temp": current_temp,
        "difference_in_temperature": difference_in_temperature,
        "chat_conclusion": chat_conclusion,
        "converted_time": converted_time,
        "converted_date": converted_date
    }


generate_weather_report()
