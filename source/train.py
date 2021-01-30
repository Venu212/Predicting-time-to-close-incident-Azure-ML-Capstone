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

from sklearn import datasets, linear_model
from time import time
import datetime
from datetime import timedelta
import time

import argparse
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import GradientBoostingRegressor

from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core.run import Run
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder


def loadData():
    #datasource = 'incident_event_log.zip'
    datasource = urlopen("https://archive.ics.uci.edu/ml/machine-learning-databases/00498/incident_event_log.zip")
    # datasource = urlopen(ds)
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
        
def clean_data(df):
    # select Incidents that are closed 
    df_closed = df[df['incident_state']=='Closed']
    df1 = df_closed[['incident_state','category','assignment_group','reopen_count',
                     'made_sla','impact','urgency','priority',
                     'opened_at','closed_at','closed_code','caused_by']]
    
    list1 = []
    for val in df1['opened_at']:
        d1 = datetime.datetime.strptime(val, "%d/%m/%Y %H:%M")
        t1 = time.mktime(d1.timetuple())
        list1.append(t1)
        
    list2 = []
    for val in df1['closed_at']:
        d2 = datetime.datetime.strptime(val, "%d/%m/%Y %H:%M")
        t2 = time.mktime(d2.timetuple())
        list2.append(t2)
        
    list3 = []
    for i in range(len(list1)):
        list3.append(list2[i]-list1[i])
        
    df1['time_to_close'] = np.array(list3)
    df1['time_to_close'] = df1['time_to_close']/3600.0
    
    priority=pd.get_dummies(df1.priority, prefix ="priority")
    df1.drop('priority', inplace=True, axis=1)
    df1= df1.join(priority)
    
    impact=pd.get_dummies(df1.impact, prefix ="impact")
    df1.drop('impact', inplace=True, axis=1)
    df1 = df1.join(impact)
    
    urgency=pd.get_dummies(df1.urgency, prefix ="urgency")
    df1.drop('urgency', inplace=True, axis=1)
    df1 = df1.join(urgency)
    
    closed_code=pd.get_dummies(df1.closed_code, prefix ="closed_code")
    df1.drop('closed_code', inplace=True, axis=1)
    df1 = df1.join(closed_code)
    
    lb_make = LabelEncoder()
    df1['category'] = lb_make.fit_transform(df1['category'])
    df1['assignment_group'] = lb_make.fit_transform(df1['assignment_group'])
    
    # df1['active']= df1['active'].astype(int)
    df1['made_sla']=df1['made_sla'].astype(int)
    
    df1 = df1.dropna()
    # df = pd.get_dummies(df)
    #df1['time_to_close'] = time_to_close
    df1 =df1.drop(['incident_state','opened_at','closed_at','caused_by'],axis=1)
    x = df1
    #X = df1.drop(['time_to_close'],axis=1)
    y= df1['time_to_close']
    return(x, y)
       
    '''
    contact_type=pd.get_dummies(df, prefix ="contact_type")
    df.drop("contact_type", inplace=True, axis=1)
    df = df.join(contact_type)
    
    category=pd.get_dummies(df, prefix ="category")
    df.drop("category", inplace=True, axis=1)
    df = df.join(category)
       
    subcategory=pd.get_dummies(df, prefix ="subcategory")
    df.drop("subcategory", inplace=True, axis=1)
    df = df.join(subcategory)
    
    symptom=pd.get_dummies(df, prefix ="symptom")
    df.drop("u_symptom", inplace=True, axis=1)
    df = df.join(symptom)
      
    assignment_group=pd.get_dummies(df, prefix ="assignment_group")
    df.drop("assignment_group", inplace=True, axis=1)
    df = df.join(assignment_group)
    
    caused_by=pd.get_dummies(df, prefix ="causedby")
    df.drop("caused_by", inplace=True, axis=1)
    df = df.join(caused_by)
    
    df = df.dropna()
    # df = pd.get_dummies(df)
    df['time_to_close'] = time_to_close
    return(df)
    '''  
  
  
def train_test_data(x,y):
    #x_train, x_test = train_test_split(dataset, test_size=0.2, random_state=10)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=11)
    return (X_train, X_test, y_train, y_test)
            

'''
def main():
    df = loadData()
    X, y = clean_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=11)
       
    
    #X_train = preprocessing.scale(X_train)
    #X_test = preprocessing.scale(X_test)
    
     # Add arguments to script
    run = Run.get_context()
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--max_depth', type=int, default=3, help="maximum depth of each tree that limits number of nodes")
    parser.add_argument('--learning_rate', type=float, default=0.1, help="Factor by which each tree's contribution shrinks")
              
    
    #parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    # parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")
    
    args = parser.parse_args()

    run.log("Regularization Strength:", np.float(args.max_depth))
    run.log("Max iterations:", np.int(args.learning_rate))
    model = GradientBoostingRegressor(max_depth=args.max_depth, learning_rate=args.learning_rate).fit(X_train, y_train)
              
    # model = linear_model.LinearRegression().fit(x_train, y_train)
    # (C=args.C, max_iter=args.max_iter)
    y_pred = model.predict(X_test)
    rms = sqrt(mean_squared_error(y_test, y_pred))

    # model = regr
    # model_name = GradientBoostingRegressor"
    # r2_score = model.score(x_test, y_test)
    rms = sqrt(mean_squared_error(y_test, y_pred))
    Rsquare = model.score(X_test, y_test)
    # Rsquare = r2_score(y_test,y_pred)
              
    
    run.log("Rsquare", np.float(Rsquare))
    run.log("rms", np.float(rms))
    run.log("Max depth:", np.float(args.max_depth))
    run.log("Learning rate:", np.int(args.learning_rate))
       
    # model = LinearRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)
    #accuracy = model.score(x_test, y_test)
    #run.log("Accuracy", np.float(accuracy)) 
    
if __name__ =='__main__':
    main()   

'''

