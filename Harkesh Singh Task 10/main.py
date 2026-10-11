from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib


app = FastAPI(title="Adult Income Prediction API")
model = joblib.load("best_income_model.pkl")

class IncomeInput(BaseModel):
    age: int = Field(..., ge=17, le=100)
    workclass: str
    fnlwgt: int = Field(..., gt=0)
    education: str
    education_num: int = Field(..., ge=1, le=16)
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int = Field(..., ge=0)
    capital_loss: int = Field(..., ge=0)
    hours_per_week: int = Field(..., ge=1, le=100)
    native_country: str

@app.get("/")
def home():
    return {"message": "Income Prediction API is running"}

@app.post("/predict")
def predict(data: IncomeInput):
    # Map API field names to the original CSV column names
    row = {
        "age": data.age,
        "workclass": data.workclass,
        "fnlwgt": data.fnlwgt,
        "education": data.education,
        "education.num": data.education_num,
        "marital.status": data.marital_status,
        "occupation": data.occupation,
        "relationship": data.relationship,
        "race": data.race,
        "sex": data.sex,
        "capital.gain": data.capital_gain,
        "capital.loss": data.capital_loss,
        "hours.per.week": data.hours_per_week,
        "native.country": data.native_country
    }

    X_new = pd.DataFrame([row])

    prediction = int(model.predict(X_new)[0])
    probability = float(model.predict_proba(X_new)[0, 1])

    return {
        "predicted_income": ">50K" if prediction == 1 else "<=50K",
        "probability_above_50K": round(probability, 4)
    }