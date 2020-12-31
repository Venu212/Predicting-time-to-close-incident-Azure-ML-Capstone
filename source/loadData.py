import pandas as pd
import numpy as np
import os
import zipfile
from glob import iglob

def loadData():
    datasource = 'incident_event_log.zip'
    #datasource = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00498/incident_event_log.zip'
    try:
        # with zipfile.ZipFile('incident_event_log.zip') as ds:
        ds = zipfile.ZipFile(datasource, 'r')
        ds.extractall()
        df = pd.read_csv('.\incident_event_log.csv')
        df = pd.read_csv(next(iglob('*.csv')))

        df1= pd.read_csv(datasource)
        return(df1)  
    except zipfile.BadZipFile:
        print('Bad zip file')
        
def main():
    df1 = loadData()
    print("df1",df1.head(3))
    df1.head()
    #print(dsn)
    print("data loaded")
    
if __name__ =='__main__':
    main()
    


