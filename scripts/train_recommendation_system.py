import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_recommendation_system():
    # Simulated dataset
    data = pd.DataFrame({
        'subject': [0, 1, 0, 1, 0],  # 0 = Math, 1 = Science
        'interest_level': [1, 2, 3, 4, 5],  # Scale of 1 to 5
        'difficulty_level': [3, 4, 5, 2, 1],  # Scale of 1 to 5
        'recommendation': [0, 1, 0, 1, 0]  # 0 = Easy tasks, 1 = Challenging tasks
    })
    X = data[['subject', 'interest_level', 'difficulty_level']]
    y = data['recommendation']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, 'models/recommendation_model.pkl')
    print("Recommendation system model trained and saved as 'recommendation_model.pkl'.")

if __name__ == '__main__':
    train_recommendation_system()
