import requests
import csv
import datetime
import os

def fetch_tv_data(base_url, start_date, report_type='north'):
    current_date = start_date
    consecutive_no_data_days = 0

    while consecutive_no_data_days < 5:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f"{base_url}?dateDiff={date_str}&reportType={report_type}"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch TV data for {date_str}. Status code: {response.status_code}")
            break
        
        data = response.json()
        print('Getting data for', date_str)
        
        if not data['hydra:member']:
            print(f"No data available for {date_str}.")
            consecutive_no_data_days += 1
        else:
            consecutive_no_data_days = 0
            for item in data['hydra:member']:
                entry = {
                    'description': item.get('description'),
                    'category': item.get('category'),
                    'channel': item.get('channel'),
                    'startTime': item.get('startTime'),
                    'rLength': item.get('rLength'),
                    'rateInK': item.get('rateInK'),
                    'date': date_str
                }
                append_to_csv(entry)
        
        current_date -= datetime.timedelta(days=1)

def fetch_weather_data(api_key, date, location='Brussels,BE'):
    timestamp = int(date.timestamp())
    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=50.8503&lon=4.3517&dt={timestamp}&appid={api_key}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch weather data for {date}. Status code: {response.status_code}")
        return None
    
    data = response.json()
    weather_info = data['current']['weather'][0]['description']
    temperature = data['current']['temp']
    
    return weather_info, temperature

def append_to_csv(entry, filename='tv_viewership_weather_data.csv'):
    headers = ['description', 'category', 'channel', 'startTime', 'rLength', 'rateInK', 'weather', 'temperature', 'date']
    
    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)
    
    print(f"Data for {entry['date']} appended to {filename}")

if __name__ == "__main__":
    base_url = "https://api.cim.be/api/cim_tv_public_results_daily_views"
    start_date = datetime.datetime(2025, 4, 3)
    #weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace with your API key
    
    fetch_tv_data(base_url, start_date)