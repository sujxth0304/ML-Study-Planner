# scripts/train_study_time_model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def generate_training_data():
    # Generate synthetic data that mimics real study patterns
    n_samples = 1000
    
    # Features that affect study time
    difficulties = np.random.randint(1, 6, n_samples)  # 1-5 difficulty levels
    topics = np.random.randint(1, 21, n_samples)      # 1-20 topics
    prior_knowledge = np.random.randint(1, 6, n_samples)  # 1-5 prior knowledge level
    
    # Calculate realistic study times (in minutes)
    base_time_per_topic = 45  # 45 minutes base time per topic
    
    study_times = []
    for diff, topic, prior in zip(difficulties, topics, prior_knowledge):
        # More difficult subjects need more time
        difficulty_factor = 1 + (diff * 0.2)
        # Prior knowledge reduces needed time
        knowledge_factor = 1 - (prior * 0.1)
        # More topics need proportionally more time
        topic_time = base_time_per_topic * topic * difficulty_factor * knowledge_factor
        # Add some random variation
        variation = np.random.normal(0, 10)
        study_times.append(max(30, topic_time + variation))
    
    # Create DataFrame
    df = pd.DataFrame({
        'difficulty': difficulties,
        'num_topics': topics,
        'prior_knowledge': prior_knowledge,
        'required_time': study_times
    })
    
    return df

def train_study_time_model():
    # Generate training data
    df = generate_training_data()
    
    # Prepare features and target
    X = df[['difficulty', 'num_topics', 'prior_knowledge']]
    y = df['required_time']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, 'models/study_time_model.pkl')
    print("Study time prediction model trained and saved")
    
    # Print model performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Train R² score: {train_score:.3f}")
    print(f"Test R² score: {test_score:.3f}")

if __name__ == '__main__':
    train_study_time_model()