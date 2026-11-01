import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

print("Starting feature engineering...")

# load dataset
data = pd.read_csv("dataset/Womens Clothing E-Commerce Reviews.csv")

print("Dataset loaded")

# get review column
texts = data["Review Text"].astype(str)

# TF-IDF
print("Creating TF-IDF features...")
tfidf = TfidfVectorizer(max_features=5000)
tfidf_features = tfidf.fit_transform(texts)

# Bag of Words
print("Creating Bag of Words features...")
bow = CountVectorizer(max_features=5000)
bow_features = bow.fit_transform(texts)

# create folder if not exists
os.makedirs("features", exist_ok=True)

print("Saving features...")

# save files
pickle.dump(tfidf_features, open("features/tfidf_features.pkl","wb"))
pickle.dump(bow_features, open("features/bow_features.pkl","wb"))
pickle.dump(tfidf, open("features/vectorizer.pkl","wb"))

print("Feature engineering completed successfully!")