import pandas as pd
import warnings
warnings.filterwarnings(action="ignore")

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

print("Starting model training...")

# load cleaned dataset
df = pd.read_csv("data/house_price_cleaned.csv")
print(f"Dataset loaded: {df.shape[0]} rows")

# drop irrelevant columns (same as notebook)
df = df.drop(columns=["longitude", "latitude"])
# label encode ocean_proximity
le = LabelEncoder()
df.ocean_proximity = le.fit_transform(df.ocean_proximity)

# define X and y
X = df.drop("median_house_value", axis=1)
y = df["median_house_value"]

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
model = RandomForestRegressor()
model.fit(X_train, y_train)
print("Training complete.")

# save model and encoder
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
joblib.dump(le, "model/label_encoder.pkl")
print("model.pkl and label_encoder.pkl saved to model/ folder.")