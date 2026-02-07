import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
import joblib

MODEL_PATH = 'data/salary_model.pkl'

def train_model():
    """
    Run this ONCE locally to generate the .pkl file.
    """
    # Load your REAL downloaded CSV here
    # Expected columns: ['JobTitle', 'State', 'Salary']
    # If you don't have one yet, skip this step and use the synthetic data.
    print("Training Random Forest...")
    
    # MOCK TRAINING DATA (Replace this with pd.read_csv)
    data = {
        'Role': ['Software Engineer', 'Data Scientist', 'Product Manager'] * 100,
        'State': ['TX', 'CA', 'NY'] * 100,
        'Salary': [90000, 140000, 130000] * 100
    }
    df = pd.DataFrame(data)
    
    # Pipeline: Encode categorical text -> Predict number
    model = make_pipeline(
        OneHotEncoder(handle_unknown='ignore'),
        RandomForestRegressor(n_estimators=50)
    )
    
    X = df[['Role', 'State']]
    y = df['Salary']
    
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def predict_salary(role, state):
    try:
        model = joblib.load(MODEL_PATH)
        # Create a 1-row DataFrame for prediction
        input_data = pd.DataFrame({'Role': [role], 'State': [state]})
        return int(model.predict(input_data)[0])
    except:
        # Fallback if model fails or file missing
        return 85000