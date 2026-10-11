import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


saved = joblib.load("income_model.pkl")
model = saved["model"]
scaler = saved["scaler"]     
columns = saved["columns"]

app = FastAPI(
    title="Adult Income Prediction API",
    description="Predicts whether a person earns >50K or <=50K per year.",
)

# Lets the HTML page (a different origin) call this API from the browser.
# "*" is fine while learning; after deploying, replace it with your website's address.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Person(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int = 0
    capital_loss: int = 0
    hours_per_week: int
    native_country: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 39,
                "workclass": "Private",
                "fnlwgt": 77516,
                "education": "Bachelors",
                "education_num": 13,
                "marital_status": "Never-married",
                "occupation": "Adm-clerical",
                "relationship": "Not-in-family",
                "race": "White",
                "sex": "Male",
                "capital_gain": 2174,
                "capital_loss": 0,
                "hours_per_week": 40,
                "native_country": "United-States",
            }
        }
    }


@app.get("/")
def home():
    return {"message": "Income Prediction API is running. Open /docs to try it."}


@app.post("/predict")
def predict(person: Person):
   
    row = {key.replace("_", "."): value for key, value in person.model_dump().items()}

    
    df = pd.DataFrame([row])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0).astype(float)
    if scaler is not None:
        df = scaler.transform(df)

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    return {
        "prediction": ">50K" if prediction == 1 else "<=50K",
        "probability_above_50k": round(probability, 3),
    }
