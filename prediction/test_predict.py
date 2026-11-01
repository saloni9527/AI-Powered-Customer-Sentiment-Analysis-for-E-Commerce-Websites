import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prediction.predict import predict_sentiment

print(predict_sentiment('this is a test review'))
