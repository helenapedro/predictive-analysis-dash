import requests
import pandas as pd

def fetch_data_from_api(endpoint):
    base_url = 'https://api.spacexdata.com/v4/'
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def fetch_rockets_data():
    return fetch_data_from_api('rockets')

def fetch_launchpads_data():
    return fetch_data_from_api('launchpads')

def fetch_payloads_data():
    return fetch_data_from_api('payloads')

def fetch_cores_data():
    return fetch_data_from_api('cores')

rockets_data = fetch_cores_data()

if rockets_data: 
    
    df = pd.DataFrame(rockets_data)  
    pd.set_option('display.max_columns', None) 
    print(df.columns)
    """ print(df)   """
    """ print(df['name'])  """
else: 
    print("No data to display")