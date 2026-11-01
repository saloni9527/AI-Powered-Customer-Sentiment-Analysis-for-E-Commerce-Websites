import numpy as np
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def build_lstm(vocab_size, max_length):
    model = Sequential()

    model.add(Embedding(input_dim=vocab_size, output_dim=128, input_length=max_length))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model


def train_lstm(X_train, X_test, y_train, y_test):

    print("🔄 Training LSTM Model...")

    # Tokenizer
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(X_train)

    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    max_length = 100

    X_train_pad = pad_sequences(X_train_seq, maxlen=max_length)
    X_test_pad = pad_sequences(X_test_seq, maxlen=max_length)

    vocab_size = 5000

    # Build model
    model = build_lstm(vocab_size, max_length)

    # Train model
    model.fit(X_train_pad, y_train, epochs=5, batch_size=32)

    # Evaluate model
    loss, accuracy = model.evaluate(X_test_pad, y_test)

    print(f"✅ LSTM Accuracy: {accuracy}")

    # Save model
    model.save("models/lstm_model.h5")

    # Save tokenizer
    with open("models/tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    print("✅ LSTM model saved successfully!")
    print("🎉 Deep Model Training Completed!")


# 🚀 MAIN (IMPORTANT)
if __name__ == "__main__":

    print("🚀 deep_models.py started...")

    # ⚠️ Replace this with your real dataset
    X_train = ["good product", "bad quality", "awesome item", "worst experience"]
    y_train = np.array([1, 0, 1, 0])

    X_test = ["nice product", "poor quality"]
    y_test = np.array([1, 0])

    train_lstm(X_train, X_test, y_train, y_test)