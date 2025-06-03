from fastapi import FastAPI, Form,HTTPException
from typing import Literal
import joblib
import numpy as np

app = FastAPI()

model = joblib.load(r"C:\Users\Avijit\Desktop\CANCER_RISK_PREDICTION\models\model.pkl")

@app.get("/")
def home():
    return {"message": "CANCER RISK PREDICTION"}

@app.post("/predict")
def predict(
    Age: int = Form(..., ge=0, description="Age of the patient in years"),
    gender: Literal['male', 'female'] = Form(..., description="Gender of the patient"),
    BMI: int = Form(...,ge=0, description="Body Mass Index of the patient"),
    Smoking: Literal['yes', 'no'] = Form(..., description="Does the patient smoke?"),
    GeneticRisk: Literal['low', 'medium', 'high'] = Form(..., description="Patient's genetic risk level for cancer"),
    PhysicalActivity: Literal['low', 'medium', 'high'] = Form(..., description="Patient's level of physical activity"),
    AlcoholIntake: Literal['low', 'medium', 'high'] = Form(..., description="Patient's level of alcohol consumption"),
    CancerHistory: Literal['yes', 'no'] = Form(..., description="Has the patient had cancer before?")
):  
    gender = 1 if gender == "male" else 0
    Smoking = 1 if Smoking == "yes" else 0
    GeneticRisk = {"low": 0, "medium": 1, "high": 2}[GeneticRisk]
    PhysicalActivity = {"low": 0, "medium": 1, "high": 2}[PhysicalActivity]
    AlcoholIntake = {"low": 0, "medium": 1, "high": 2}[AlcoholIntake]
    CancerHistory = 1 if CancerHistory == "yes" else 0
    try:
     input = np.array([[Age, gender, BMI, Smoking, GeneticRisk, PhysicalActivity, AlcoholIntake, CancerHistory]])
     value = model.predict(input)[0]
    except:
       raise HTTPException(status_code=500,detail="machine learning model is not found")

    if value == 1:
        return {"result : CANCER DETECTED"}
    else:
        return {"result : PATIENT IS SAFE"}
