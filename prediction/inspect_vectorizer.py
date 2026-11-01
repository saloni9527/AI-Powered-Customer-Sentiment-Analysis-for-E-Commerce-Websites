import os
import pickle
from sklearn.utils.validation import check_is_fitted

base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(base, 'models', 'model.pkl')
vec_path = os.path.join(base, 'models', 'vectorizer.pkl')
print('model exists', os.path.isfile(model_path))
print('vectorizer exists', os.path.isfile(vec_path))
with open(vec_path, 'rb') as f:
    vec = pickle.load(f)
print('vectorizer type', type(vec))
try:
    check_is_fitted(vec)
    print('vectorizer fitted yes')
except Exception as e:
    print('vectorizer fitted error', type(e).__name__, e)
print('has idf_', hasattr(vec, 'idf_'))
print('attributes', [a for a in dir(vec) if a.endswith('_')][:20])
