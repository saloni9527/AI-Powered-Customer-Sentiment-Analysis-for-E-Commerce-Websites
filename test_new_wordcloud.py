#!/usr/bin/env python
"""Test the new get_all_sentiment_words function."""
import sys
sys.path.insert(0, '.')

from app import get_all_sentiment_words

# Test 1: Sample reviews
test_reviews = [
    {"text": "This product is amazing and works great! Love it", "sentiment": "Positive"},
    {"text": "Very disappointed with the quality and delivery", "sentiment": "Negative"},
    {"text": "Good product overall, nothing special", "sentiment": "Positive"},
    {"text": "Not bad but could be better quality", "sentiment": "Neutral"},
    {"text": "Love this! Best purchase ever made", "sentiment": "Positive"},
    {"text": "Terrible experience, very unhappy", "sentiment": "Negative"},
]

print("=" * 60)
print("TEST 1: Sample reviews")
print("=" * 60)
result = get_all_sentiment_words(test_reviews)
print(f"Type: {type(result)}")
print(f"Length: {len(result)}")
if result:
    print(f"Sample items:")
    for item in result[:5]:
        print(f"  {item}")
else:
    print("Result is empty!")

# Test 2: Empty reviews
print("\n" + "=" * 60)
print("TEST 2: Empty reviews")
print("=" * 60)
result = get_all_sentiment_words([])
print(f"Result: {result}")

# Test 3: All stopwords (should return original words)
print("\n" + "=" * 60)
print("TEST 3: All stopwords (fallback test)")
print("=" * 60)
stopword_reviews = [
    {"text": "the and for with that this was from have", "sentiment": "Positive"},
]
result = get_all_sentiment_words(stopword_reviews)
print(f"Type: {type(result)}")
print(f"Length: {len(result)}")
if result:
    print(f"Words: {result}")
