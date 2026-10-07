from fastapi import FastAPI,HTTPException
from typing import Optional,Annotated,Literal
from pydantic import BaseModel,Field,field_validator

['Age', 'Gender', 'Country', 'Academic_Level', 'Most_Used_Platform',
       'Purpose_Of_Use', 'Avg_Daily_Usage_Hours', 'Daily_Unlocks',
       'Study_Hours', 'Physical_Activity_Hours', 'Sleep_Hours_Per_Night',
       'Stress_Level']

country=['Other', 'Canada', 'USA', 'India', 'Australia', 'UK', 'Germany',
       'France', 'Mexico', 'Turkey']

class Mental_health(BaseModel):
    Age:Annotated[int,Field(...,gt=5,lt=25)]
    Gender:Annotated[Literal['Male','Female'],Field(...)]
    Country:Annotated[Literal['Other', 'Canada', 'USA', 'India', 'Australia', 'UK', 'Germany',
       'France', 'Mexico', 'Turkey'],Field(...)]
    Academic_Level:Annotated[Literal['Undergraduate', 'Graduate', 'High School'],Field(...)]
    Most_Used_Platform:Annotated[Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
       'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp',
       'WeChat'],Field(...)]
    Purpose_Of_Use:Annotated[Literal['Networking', 'Education', 'Entertainment', 'News'],Field(...)]
    Avg_Daily_Usage_Hours:Annotated[int,Field(...,ge=0,le=20)]
    Daily_Unlocks:Annotated[float,Field(...,gt=0,lt=300)]
    Study_Hours:Annotated[float,Field(...,gt=0,lt=16)]
    Physical_Activity_Hours:Annotated[float,Field(...,ge=0,lt=20)]
    Sleep_Hours_Per_Night:Annotated[float,Field(...,gt=1,lt=19)]
    Stress_Level:Annotated[Literal['Medium', 'Low', 'Very High', 'High'],Field(...)]
    @field_validator('Country',mode='before')
    @classmethod
    def check_valid_country(cls, value: str) -> str:
        if value not in country:
            return 'Other'
        else:
            return value
class Mental_health_response(BaseModel):
    Mental_health_score:float
