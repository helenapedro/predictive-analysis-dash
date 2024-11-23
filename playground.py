import pandas as pd
from utils.data import fetch_static_data

def fetch_and_process_data():
     static_data = fetch_static_data()
     
     if static_data: 
          df = pd.DataFrame(static_data)  
          pd.set_option('display.max_columns', None)
          print(df.columns) 

          """ print(df.columns)
          print(df.dtypes)
          print(df.head)
          print(df) """
          """ print(df.columns) """
          """ print(df['rocket']) """
     else: 
          print("No data to display")

""" rockets_data = fetch_rockets_data()
rocket_id_to_name = {rocket['id']: rocket['name'] for rocket in rockets_data}
 """

""" def getBoosterVersion(rockets_data):
    global BoosterVersion
    BoosterVersion = [item['rocket'].get('rocket_name', 'Unknown') for item in rockets_data]
    return BoosterVersion """

""" def getBoosterVersion(rockets_data, rockets_mapping):
    global BoosterVersion
    BoosterVersion = [rockets_mapping.get(item['rocket'], 'Unknown') for item in rockets_data]
    return BoosterVersion

 """
