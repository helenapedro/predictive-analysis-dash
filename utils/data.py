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



def fetch_static_data_from_api(endpoint):
    base_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/'
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    
def fetch_rocket_launch_data():
    return fetch_static_data_from_api('API_call_spacex_api.json')

rockets__launch = fetch_rocket_launch_data()
rockets_data = fetch_rockets_data()
rocket_id_to_name = {rocket['id']: rocket['name'] for rocket in rockets_data}


""" def getBoosterVersion(rockets_data):
    global BoosterVersion
    BoosterVersion = [item['rocket'].get('rocket_name', 'Unknown') for item in rockets_data]
    return BoosterVersion """

def getBoosterVersion(rockets_data, rockets_mapping):
    global BoosterVersion
    BoosterVersion = [rockets_mapping.get(item['rocket'], 'Unknown') for item in rockets_data]
    return BoosterVersion



if rockets_data: 
    
    df = pd.DataFrame(rockets_data)  
    pd.set_option('display.max_columns', None) 

    """ print(df.columns)
    print(df.dtypes)
    print(df.head)
    print(df) """
    """ print(df.columns) """
    """ print(df['rocket']) """
else: 
    print("No data to display")