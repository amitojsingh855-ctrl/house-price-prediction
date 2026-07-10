from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import PredictionHistory
from schemas import HouseInput
import joblib
import pandas as pd

# auto create prediction_history table in Neon on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="House Price Prediction API")

# load ML model and label encoder at startup
# both files must be inside the model/ folder
model = joblib.load("model/model.pkl")
le    = joblib.load("model/label_encoder.pkl")


# Home API
@app.get("/")
def home():
    return {"message": "House Price Prediction API is running"}


# Predict API
@app.post("/predict")
def predict(data: HouseInput, db: Session = Depends(get_db)):

    # encode ocean_proximity using the same label encoder used during training
    ocean_encoded = le.transform([data.ocean_proximity])[0]

    # build input dataframe matching exact column order from training
    input_df = pd.DataFrame([{
        "housing_median_age": data.housing_median_age,
        "total_rooms":        data.total_rooms,
        "total_bedrooms":     data.total_bedrooms,
        "population":         data.population,
        "households":         data.households,
        "median_income":      data.median_income,
        "ocean_proximity":    ocean_encoded
    }])

    # predict using loaded ML model
    predicted_price = model.predict(input_df)[0]

    # store prediction in Neon PostgreSQL prediction_history table
    record = PredictionHistory(
        housing_median_age = data.housing_median_age,
        total_rooms        = data.total_rooms,
        total_bedrooms     = data.total_bedrooms,
        population         = data.population,
        households         = data.households,
        median_income      = data.median_income,
        ocean_proximity    = data.ocean_proximity,
        predicted_price    = round(float(predicted_price), 2)
    )
    db.add(record)
    db.commit()

    return {
        "predicted_price": round(float(predicted_price), 2),
        "message": "Prediction stored successfully"
    }


# View last 10 predictions — Bonus feature
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(PredictionHistory).order_by(
        PredictionHistory.id.desc()
    ).limit(10).all()
    return records