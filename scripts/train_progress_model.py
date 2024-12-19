import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

def train_progress_model():
    # Simulated dataset
    data = pd.DataFrame({
        'study_hours': [1, 2, 3, 4, 5],
        'progress_score': [10, 20, 30, 40, 50]  # Example linear relationship
    })
    X = data[['study_hours']]
    y = data['progress_score']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, 'models/progress_model.pkl')
    print("Progress model trained and saved as 'progress_model.pkl'.")

if __name__ == '__main__':
    train_progress_model()
