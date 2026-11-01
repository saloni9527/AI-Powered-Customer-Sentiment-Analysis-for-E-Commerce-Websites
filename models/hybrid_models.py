import numpy as np
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


# 🔹 Step 1: Build CNN Feature Extractor
def build_cnn(vocab_size, max_length):

    model = Sequential()

    model.add(Embedding(input_dim=vocab_size, output_dim=128, input_length=max_length))
    model.add(Conv1D(filters=128, kernel_size=5, activation='relu'))
    model.add(GlobalMaxPooling1D())

    return model


# 🔹 Step 2: Hybrid Training Function
def train_hybrid_model(X_train, X_test, y_train, y_test):

    print("🚀 Training Hybrid Model (CNN + SVM)...")

    # Tokenization
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(X_train)

    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    max_length = 100

    X_train_pad = pad_sequences(X_train_seq, maxlen=max_length)
    X_test_pad = pad_sequences(X_test_seq, maxlen=max_length)

    vocab_size = 5000

    # CNN Feature Extractor
    cnn_model = build_cnn(vocab_size, max_length)

    # Extract features
    train_features = cnn_model.predict(X_train_pad)
    test_features = cnn_model.predict(X_test_pad)

    # SVM Classifier
    svm = SVC()

    print("🔄 Training SVM on CNN features...")
    svm.fit(train_features, y_train)

    # Prediction
    predictions = svm.predict(test_features)

    accuracy = accuracy_score(y_test, predictions)

    print(f"✅ Hybrid Model Accuracy: {accuracy}")

    # Save SVM model
    with open("models/hybrid_svm.pkl", "wb") as f:
        pickle.dump(svm, f)

    # Save tokenizer
    with open("models/hybrid_tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    print("✅ Hybrid model saved successfully!")
    print("🎉 Hybrid Model Training Completed!")


# 🚀 MAIN
if __name__ == "__main__":

    print("🚀 hybrid_models.py started...")

    # ⚠️ Replace with real dataset later
    X_train = ["good product", "bad quality", "excellent item", "worst experience"]
    y_train = np.array([1, 0, 1, 0])

    X_test = ["nice product", "poor item"]
    y_test = np.array([1, 0])

    train_hybrid_model(X_train, X_test, y_train, y_test)