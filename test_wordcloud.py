#!/usr/bin/env python
"""Quick test of get_all_sentiment_words function."""

import sys
sys.path.insert(0, '.')

from app import get_all_sentiment_words

# Test with sample data
test_reviews = [
    {"text": "This product is amazing and works great!", "sentiment": "Positive"},
    {"text": "Very disappointed with the quality", "sentiment": "Negative"},
    {"text": "Good product overall", "sentiment": "Positive"},
    {"text": "Not bad but could be better", "sentiment": "Neutral"},
    {"text": "Love this! Best purchase ever", "sentiment": "Positive"},
    {"text": "Terrible experience, very unhappy", "sentiment": "Negative"},
    {"text": "This is exactly what I was looking for", "sentiment": "Positive"},
    {"text": "Average product, nothing special", "sentiment": "Neutral"},
]

print("Testing get_all_sentiment_words with sample data...")
result = get_all_sentiment_words(test_reviews)
print(f"Result type: {type(result)}")
print(f"Result length: {len(result) if isinstance(result, list) else 'not a list'}")
if isinstance(result, list) and len(result) > 0:
    print(f"First item: {result[0]}")
    print(f"Sample items ({min(5, len(result))} of {len(result)}):")
    for item in result[:5]:
        print(f"  - {item['text']:20} size={item['size']:3} color={item['color']:6} sent={item['sentiment']}")
else:
    print(f"Result: {result}")
