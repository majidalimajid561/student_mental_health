from fastapi  import FastAPI
from schema.user_input import Mental_health,Mental_health_response
from modling.predict import prediction,model_version
from fastapi.middleware.cors import  CORSMiddleware

app=FastAPI()


app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])
@app.get('/')
def home():
    return "this is mental heath API"

@app.get('/health')
def heatlh():
    return {'status':'True','model':'loaded'}
@app.post('/predict',response_model=Mental_health_response)
def model_predtion(data:Mental_health):
    input={
        'Age':data.Age,
        'Gender':data.Gender,
        'Country':data.Country,
        'Academic_Level':data.Academic_Level,
        'Most_Used_Platform':data.Most_Used_Platform,
        'Purpose_Of_Use':data.Purpose_Of_Use,
        'Avg_Daily_Usage_Hours':data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks':data.Daily_Unlocks,
        'Study_Hours':data.Study_Hours,
        'Physical_Activity_Hours':data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night':data.Sleep_Hours_Per_Night,
        'Stress_Level':data.Stress_Level}
    result=prediction(input)
    return Mental_health_response(Mental_health_score=round(result,2))