import joblib
import numpy as np
import pandas as pd
mode=None
try:
    with open('../models/random_forest.pkl','rb') as f:
        model=joblib.load(f)
        model_version='1.0.0'
        print("model loaded")
except Exception as e:
    raise FileNotFoundError(f'model  file nai meli{e}')
def prediction(data:dict)-> float:
    if model==None:
       return "Model load to howa nai"
    try:
     input_data=pd.DataFrame([data])
     result=model.predict(input_data)[0]
     return result
    except Exception as e:
      raise Exception(f'model fail in prediction {e}')
    
