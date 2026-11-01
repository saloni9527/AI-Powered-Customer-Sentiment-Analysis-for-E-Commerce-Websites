import json
import math
import os
import pickle
import re
from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ================= PATH SETUP =================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")


# ================= CLEAN TEXT =================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()


# ================= SENTIMENT CONVERSION =================
def convert_sentiment(score):
    try:
        score = float(score)
    except:
        return "Neutral"

    if score <= 2:
        return "Negative"
    elif score == 3:
        return "Neutral"
    else:
        return "Positive"


# ================= STANDARDIZE DATA =================
def process_dataframe(df):
    df.columns = df.columns.str.lower()

    # Detect text column
    if "review" in df.columns:
        df.rename(columns={"review": "Text"}, inplace=True)
    elif "text" in df.columns:
        df.rename(columns={"text": "Text"}, inplace=True)
    elif "content" in df.columns:
        df.rename(columns={"content": "Text"}, inplace=True)
    else:
        return None

    # Detect score column
    if "rating" in df.columns:
        df.rename(columns={"rating": "Score"}, inplace=True)
    elif "score" in df.columns:
        df.rename(columns={"score": "Score"}, inplace=True)
    elif "sentiment" in df.columns:
        # Some datasets already contain sentiment labels.
        df.rename(columns={"sentiment": "Sentiment"}, inplace=True)
        df = df[["Text", "Sentiment"]].dropna()
        df["Text"] = df["Text"].apply(clean_text)
        df["Sentiment"] = df["Sentiment"].astype(str).str.strip().str.capitalize()
        df = df[df["Sentiment"].isin(["Positive", "Neutral", "Negative"])]
        return df
    else:
        return None

    df = df[["Text", "Score"]].dropna()
    df["Text"] = df["Text"].apply(clean_text)
    df["Sentiment"] = df["Score"].apply(convert_sentiment)

    return df


# ================= LOAD ALL DATASETS =================
def load_all_datasets():
    train_list = []
    test_list = []

    def find_split_csv(site_path, split_name):
        """
        Find train/test CSV in common folder structures:
        - site/train/train.csv
        - site/Train/Train.csv
        - site/train.csv
        """
        split_lower = split_name.lower()
        candidates = []

        # Direct file in site root (e.g., Meesho/train.csv)
        for name in (f"{split_lower}.csv", f"{split_name}.csv", f"{split_name.capitalize()}.csv"):
            candidates.append(os.path.join(site_path, name))

        # File inside split folder (e.g., site/Train/Train.csv)
        for folder in os.listdir(site_path):
            folder_path = os.path.join(site_path, folder)
            if not os.path.isdir(folder_path):
                continue
            if folder.lower() != split_lower:
                continue
            for file_name in os.listdir(folder_path):
                if file_name.lower() == f"{split_lower}.csv":
                    candidates.append(os.path.join(folder_path, file_name))

        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    for site in os.listdir(DATASET_DIR):
        site_path = os.path.join(DATASET_DIR, site)

        if not os.path.isdir(site_path):
            continue

        train_file = find_split_csv(site_path, "train")
        test_file = find_split_csv(site_path, "test")

        # Load TRAIN
        if train_file and os.path.exists(train_file):
            df = pd.read_csv(train_file)
            df = process_dataframe(df)
            if df is not None:
                train_list.append(df)

        # Load TEST
        if test_file and os.path.exists(test_file):
            df = pd.read_csv(test_file)
            df = process_dataframe(df)
            if df is not None:
                test_list.append(df)

    if len(train_list) == 0:
        raise Exception("No train datasets found!")

    train_df = pd.concat(train_list, ignore_index=True)

    if len(test_list) > 0:
        test_df = pd.concat(test_list, ignore_index=True)
    else:
        test_df = None

    return train_df, test_df


# ================= TRAIN MODEL =================
def train_model():
    print("Loading datasets...")
    train_df, test_df = load_all_datasets()

    print("Train size:", len(train_df))

    # Balance dataset
    min_count = train_df["Sentiment"].value_counts().min()

    train_df = pd.concat([
        train_df[train_df["Sentiment"] == "Positive"].sample(min_count, random_state=42),
        train_df[train_df["Sentiment"] == "Negative"].sample(min_count, random_state=42),
        train_df[train_df["Sentiment"] == "Neutral"].sample(min_count, random_state=42)
    ]).sample(frac=1, random_state=42)

    X_train = train_df["Text"]
    y_train = train_df["Sentiment"]

    # Vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)

    # Model
    model = LogisticRegression(max_iter=500, class_weight="balanced")
    model.fit(X_train_vec, y_train)

    print("Training completed")

    # ================= TEST =================
    if test_df is not None:
        print("\nEvaluating on test data...")

        X_test = test_df["Text"]
        y_test = test_df["Sentiment"]

        X_test_vec = vectorizer.transform(X_test)
        y_pred = model.predict(X_test_vec)

        print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # ================= SAVE =================
    os.makedirs(MODELS_DIR, exist_ok=True)

    with open(os.path.join(MODELS_DIR, "model.pkl"), "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    print("\nModel saved successfully!")


def batch_reviews(items, batch_size=100):
    for start in range(0, len(items), batch_size):
        yield items[start: start + batch_size]


def extract_top_keywords(texts, top_n=20):
    if len(texts) == 0:
        return []

    vectorizer = CountVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
    matrix = vectorizer.fit_transform(texts)
    counts = matrix.sum(axis=0).A1
    features = vectorizer.get_feature_names_out()
    keywords = sorted(zip(features, counts), key=lambda x: x[1], reverse=True)
    return [word for word, _ in keywords[:top_n]]


def sentiment_counts(df):
    counts = df["Sentiment"].value_counts().to_dict()
    return {
        "Positive": counts.get("Positive", 0),
        "Neutral": counts.get("Neutral", 0),
        "Negative": counts.get("Negative", 0),
    }


def get_top_sentiment_keywords(df, label, top_n=10):
    subset = df[df["Sentiment"] == label]
    return extract_top_keywords(subset["Text"].tolist(), top_n=top_n)


def generate_actionable_insights(overall, themes, positive_phrases, negative_phrases):
    insights = []
    total = overall["Positive"] + overall["Neutral"] + overall["Negative"]

    if total == 0:
        return ["No reviews available for analysis."]

    if overall["Negative"] / total > 0.25:
        insights.append("High negative sentiment detected - investigate product quality, shipping, and customer support.")
    else:
        insights.append("Negative sentiment is moderate; focus on the most frequent complaint themes.")

    if overall["Positive"] / total >= 0.5:
        insights.append("Positive sentiment dominates; highlight the top praised features in marketing.")

    if "battery" in themes or "power" in themes:
        insights.append("Battery or power-related feedback is common - consider improving battery life messaging.")
    if "shipping" in themes or "delivery" in themes:
        insights.append("Delivery experience is a recurring theme - review logistics and packaging.")
    if "quality" in themes:
        insights.append("Product quality appears in themes; use this to prioritize QA and feature improvements.")

    insights.append(f"Top themes: {', '.join(themes[:5])}")
    insights.append(f"Top positive phrases: {', '.join(positive_phrases[:5])}")
    insights.append(f"Top negative phrases: {', '.join(negative_phrases[:5])}")
    return insights


def analyze_reviews_batch(file_path="dataset/reviews.csv", batch_size=100, save_summary=True):
    print("Loading review dataset for workflow analysis...")
    df = pd.read_csv(file_path)
    df = process_dataframe(df)

    if df is None or len(df) == 0:
        raise Exception("No valid review data found for workflow analysis.")

    total_reviews = len(df)
    print(f"Total reviews loaded: {total_reviews}")
    overall_counts = sentiment_counts(df)
    print("Overall sentiment:", overall_counts)

    batches = list(batch_reviews(df.to_dict(orient="records"), batch_size=batch_size))
    batch_summaries = []

    for batch_index, batch in enumerate(batches, start=1):
        batch_df = pd.DataFrame(batch)
        batch_counts = sentiment_counts(batch_df)
        batch_keywords = extract_top_keywords(batch_df["Text"].tolist(), top_n=10)
        batch_summaries.append({
            "batch": batch_index,
            "size": len(batch),
            "sentiment": batch_counts,
            "themes": batch_keywords,
        })
        if batch_index <= 5 or batch_index % 50 == 0 or batch_index == len(batches):
            print(f"Batch {batch_index}/{len(batches)} processed - size={len(batch)}, sentiment={batch_counts}")

    top_themes = extract_top_keywords(df["Text"].tolist(), top_n=20)
    positive_phrases = get_top_sentiment_keywords(df, "Positive", top_n=10)
    negative_phrases = get_top_sentiment_keywords(df, "Negative", top_n=10)
    insights = generate_actionable_insights(overall_counts, top_themes, positive_phrases, negative_phrases)

    summary = {
        "total_reviews": total_reviews,
        "batch_size": batch_size,
        "batches": len(batches),
        "overall_sentiment": overall_counts,
        "top_themes": top_themes,
        "top_positive_phrases": positive_phrases,
        "top_negative_phrases": negative_phrases,
        "actionable_insights": insights,
        "batch_summaries": batch_summaries,
    }

    if save_summary:
        out_path = os.path.join(PROJECT_ROOT, "workflow_review_summary.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\nWorkflow summary saved to {out_path}")

    return summary


def display_summary(summary):
    print("\n=== Workflow Summary ===")
    print("Total reviews:", summary["total_reviews"])
    print("Batches:", summary["batches"], "batch size:", summary["batch_size"])
    print("Overall sentiment:", summary["overall_sentiment"])
    print("Top themes:", ", ".join(summary["top_themes"][:10]))
    print("Actionable insights:")
    for insight in summary["actionable_insights"]:
        print(" -", insight)


# ================= RUN =================
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "workflow":
        batch = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        summary = analyze_reviews_batch(batch_size=batch)
        display_summary(summary)
    else:
        train_model()