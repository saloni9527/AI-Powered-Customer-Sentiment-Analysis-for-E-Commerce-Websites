import importlib.util
import os
import pickle
import re
import threading

from sklearn.exceptions import NotFittedError
from sklearn.utils.validation import check_is_fitted

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL_PATH = os.path.join(_BASE, "models", "model.pkl")
_VECTORIZER_PATH = os.path.join(_BASE, "models", "vectorizer.pkl")

_model = None
_vectorizer = None
_load_lock = threading.Lock()


def _load_pickles():
    global _model, _vectorizer
    with open(_MODEL_PATH, "rb") as f:
        _model = pickle.load(f)
    with open(_VECTORIZER_PATH, "rb") as f:
        _vectorizer = pickle.load(f)


def _vectorizer_is_fitted(vectorizer) -> bool:
    if vectorizer is None:
        return False
    try:
        if hasattr(vectorizer, "idf_"):
            check_is_fitted(vectorizer, attributes=["idf_"])
        else:
            check_is_fitted(vectorizer)
        return True
    except (NotFittedError, AttributeError):
        return False


def _retrain_models():
    """Rebuild model.pkl and vectorizer.pkl using the project train_model.py."""
    path = os.path.join(_BASE, "train_model.py")
    if not os.path.isfile(path):
        raise RuntimeError(
            f"TF-IDF vectorizer is not fitted and train_model.py was not found at {path}. "
            "Run from the project folder: python train_model.py"
        )
    spec = importlib.util.spec_from_file_location("train_model", path)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    if not hasattr(tm, "train_model"):
        raise RuntimeError(
            "The train_model.py module does not expose a train_model() function. "
            "Update train_model.py or the prediction fallback logic."
        )
    tm.train_model()


def _ensure_models():
    """Load pickles; if vectorizer is unfitted (common bad artifact), retrain once."""
    global _model, _vectorizer
    if _model is not None and _vectorizer is not None and _vectorizer_is_fitted(_vectorizer):
        return

    with _load_lock:
        if _model is not None and _vectorizer is not None and _vectorizer_is_fitted(_vectorizer):
            return

        if not os.path.isfile(_MODEL_PATH) or not os.path.isfile(_VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Missing {_MODEL_PATH!r} or {_VECTORIZER_PATH!r}. "
                "Run from the project folder: python train_model.py"
            )

        _load_pickles()
        if _vectorizer_is_fitted(_vectorizer):
            return

        _retrain_models()
        _load_pickles()
        if not _vectorizer_is_fitted(_vectorizer):
            raise RuntimeError(
                "The TF-IDF vectorizer is still not fitted after training. "
                "Try deleting models/vectorizer.pkl and models/model.pkl, then run: python train_model.py"
            )


def _clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()


def predict_sentiment(review):
    _ensure_models()
    cleaned = _clean_text(review)
    try:
        data = _vectorizer.transform([cleaned])
    except NotFittedError:
        # If the loaded vectorizer somehow isn't fitted, retrain and reload.
        _retrain_models()
        _load_pickles()
        data = _vectorizer.transform([cleaned])
    prediction = _model.predict(data)[0]
    return prediction


# Backward compatibility: allow `from prediction.predict import model, vectorizer`
def __getattr__(name):
    if name == "model":
        _ensure_models()
        return _model
    if name == "vectorizer":
        _ensure_models()
        return _vectorizer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
