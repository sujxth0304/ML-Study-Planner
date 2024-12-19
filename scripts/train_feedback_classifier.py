import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib

def train_feedback_classifier():
    # Simulated dataset
    data = pd.DataFrame({
        'feedback_text': [
            'This plan is perfect!',
            'I need more breaks',
            'Content is too hard',
            'It’s too easy',
            'Exactly what I needed'
        ],
        'feedback_label': [1, 0, 0, 0, 1]  # 1 = Positive, 0 = Negative
    })
    X = data['feedback_text']
    y = data['feedback_label']

    # Text vectorization
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    # Train model
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    # Save model and vectorizer
    joblib.dump(classifier, 'models/feedback_classifier.pkl')
    joblib.dump(vectorizer, 'models/feedback_vectorizer.pkl')
    print("Feedback classifier trained and saved as 'feedback_classifier.pkl'.")

if __name__ == '__main__':
    train_feedback_classifier()
