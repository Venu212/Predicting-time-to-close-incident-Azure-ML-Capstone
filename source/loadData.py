import pandas as pd
import numpy as np
import os
import zipfile
from zipfile import ZipFile
from zipfile import BadZipFile
from glob import iglob
from io import BytesIO
from urllib.request import urlopen

import dateutil.parser
from sklearn.model_selection import train_test_split


def loadData(datasource):
    #datasource = 'incident_event_log.zip'
    # datasource = urlopen("https://archive.ics.uci.edu/ml/machine-learning-databases/00498/incident_event_log.zip")
    #datasource = urlopen(incident)
    try:
        # with zipfile.ZipFile('incident_event_log.zip') as ds:
        ds = ZipFile(BytesIO(datasource.read()))
        ds.extractall()
        ds.namelist()
        #df = pd.read_csv(zipfile.open('incident_event_log.csv')
        df = pd.read_csv(next(iglob('*.csv')))
        return(df)  
    except zipfile.BadZipFile:
        print('Bad zip file')

def select_features_target(dataset):
    df = dataset
    df.astype({
        'opened_at':'datetime64',
        'sys_created_at':'datetime64',
        'sys_updated_at':'datetime64',
        'sys_updated_at':'datetime64',
        'resolved_at':'datetime64',
        'closed_at':'datatime64'}).dtypes
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['opened_at'] = pd.to_datetime(df['opened_at'])
    df['days_to_close'] = (df['closed_at'] - df['opened_at'])
    df['days_to_close'].dt.components.days
    df.remove('closed_at', 'resolved_at')
    x = df.remove('days_to_close')
    y = df['days_to_close']
    return(x,y)

def train_test_data(x,y):
    #x_train, x_test = train_test_split(dataset, test_size=0.2, random_state=10)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, 
                                                        random_state=11)
    
    return (x_train, x_test, y_train, y_test)
            

  
'''
def main():
    df1 = loadData()
    #print("df1",df1.head(3))
    df1.head()
    #print(dsn)
    #print("data loaded")
    
if __name__ =='__main__':
    main()   
'''

