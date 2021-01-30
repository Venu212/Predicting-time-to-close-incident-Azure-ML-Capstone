import pickle
import joblib
import numpy as np
import os
import azureml.train.automl
from azureml.core import Model 
import json
import pandas as pd

# from sklearn.externals import joblib

# from inference_schema.schema_decorators import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType


# The init() method is called once, when the web service starts up.
#
# Typically you would deserialize the model file, as shown here using joblib,
# and store it in a global variable so your run() method can access it later.

 
def init():
    
    # retrieve the path to the model file using the model name
    model_name = 'automl_best_model'

    global model
    
    model_path = Model.get_model_path(model_name)
    model = joblib.load(model_path)


    # model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], model_name)
    # ~/cloudfiles/code/Users/Raji_challa/automl_best_model.txt
    # model_path =Model.get_model_path('automl_best_model.txt')
    # model_loaded = joblib.load(model_path)
   

def run(data):
    try:
        data_js = json.loads(data)
        data = pd.DataFrame(data_js['data'])
        result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
'''
def run(data):
    try:
        result = model.predict(data)
        # you can return any datatype as long as it is JSON-serializable
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error


def init():
    global model

    # The AZUREML_MODEL_DIR environment variable indicates
    # a directory containing the model file you registered.
    model_filename = 'optimal_model.joblib'
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], model_filename)

    model = joblib.load(model_path)


# The run() method is called each time a request is made to the scoring API.
#
# Shown here are the optional input_schema and output_schema decorators
# from the inference-schema pip package. Using these decorators on your
# run() method parses and validates the incoming payload against
# the example input you provide here. This will also generate a Swagger
# API document for your web service.
@input_schema('data', NumpyParameterType(np.array([[0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.0]])))
@output_schema(NumpyParameterType(np.array([4429.929236457418])))
def run(data):
    # Use the model object loaded by init().
    result = model.predict(data)

    # You can return any JSON-serializable object.
    return result.tolist()
'''