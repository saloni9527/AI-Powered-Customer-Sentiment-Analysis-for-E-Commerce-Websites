"""Verify package modules import and basic functions work."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_prediction_sentiment():
    from prediction.predict import predict_sentiment

    label = predict_sentiment("Great product, love the quality and shipping was fast")
    assert label is not None


def test_app_helpers_importable_with_app():
    import app as m

    assert m.validate_name("John")[0] is True
    assert m.validate_name("J")[0] is False
    ok, em = m.validate_email("bad")
    assert ok is False
    ok, em = m.validate_email("test@example.com")
    assert ok is True
    assert m._mask_rainforest_key("abcd1234efgh5678") == "abcd…5678 (16 chars)"
    assert m.classify_sentiment("I love this")[0] in ("POSITIVE", "NEGATIVE", "NEUTRAL")


def test_extract_amazon_asin():
    import app as m

    u = "https://www.amazon.in/dp/B0GTTXP6WF"
    assert m.extract_amazon_asin(u) == "B0GTTXP6WF"


def test_flipkart_url_helpers():
    import app as m

    u = "https://flipkart.com/item-name/p/itm1234567890abcdef?utm_source=x&otracker=cl"
    n = m.normalize_flipkart_product_url(u)
    assert "www.flipkart.com" in n
    assert "utm_source" not in n.lower()
    rev = m.flipkart_product_reviews_url("https://www.flipkart.com/item-name/p/itm1234567890abcdef")
    assert rev and "product-reviews" in rev


def test_flask_url_map_has_core_routes(flask_app):
    rules = {str(r.rule) for r in flask_app.url_map.iter_rules()}
    assert "/sklearn-analytics" in rules
    assert "/product" in rules
    assert "/api/trends" in rules
