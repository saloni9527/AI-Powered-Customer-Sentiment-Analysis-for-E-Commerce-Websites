import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
data = pd.read_csv('dataset/Womens Clothing E-Commerce Reviews.csv')
data = data.dropna(subset=['Review Text'])
data['sentiment'] = data['Rating'].apply(lambda x: 1 if x >= 4 else 0)

X = data['Review Text']
y = data['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Save
pickle.dump(model, open('models/LogisticRegression.pkl', 'wb'))
pickle.dump(vectorizer, open('features/vectorizer.pkl', 'wb'))

print("Model and vectorizer saved")