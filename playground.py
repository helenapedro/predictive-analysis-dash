import pandas as pd # type: ignore
from prettytable import PrettyTable # type: ignore
from utils.data import fetch_static_data

def fetch_and_process_data():
    static_data = fetch_static_data()
    if static_data:
        df = pd.DataFrame(static_data)
        pd.set_option('display.max_columns', None)
        
        print("-----------------------DF COLUMNS--------------------------")
        print(df.columns)
        print("-----------------------DF HEAD--------------------------")
        
        # Create a PrettyTable object
        table = PrettyTable()
        table.field_names = df.columns.tolist()  # Set column headers
        for row in df.head(5).itertuples(index=False):
            table.add_row(row)  # Add rows to the table
        
        print(table)
        
        print("-----------------------DF DTYPES--------------------------")
        print(df.dtypes)
        print("-----------------------ROCKET Column--------------------------")
        print(df['rocket'])
        print("-----------------------ROCKET ID TO NAME--------------------------")
        """ 
        Add additional transformations or logic if required.
        """
    else: 
        print("No data to display")

""" static_data = fetch_and_process_data() """


""" def getBoosterVersion(rockets_data):
    global BoosterVersion
    BoosterVersion = [item['rocket'].get('rocket_name', 'Unknown') for item in rockets_data]
    return BoosterVersion """

""" def getBoosterVersion(rockets_data, rockets_mapping):
    global BoosterVersion
    BoosterVersion = [rockets_mapping.get(item['rocket'], 'Unknown') for item in rockets_data]
    return BoosterVersion

 """