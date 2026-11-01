"""Smoke tests for main HTTP routes (Flask test client — no separate server)."""
import os

import pytest


@pytest.mark.parametrize(
    "path,expect",
    [
        ("/", 200),
        ("/about", 200),
        ("/contact", 200),
        ("/auth/login", 200),
        ("/auth/signup", 200),
        ("/legacy/text", 200),
        ("/product", 200),
        ("/results", 200),
        ("/history", 200),
        ("/sklearn-analytics", 200),
        ("/api/trends", 200),
        ("/export/json", 200),
        ("/export/csv", 200),
        ("/api/dashboard-stats", 200),
    ],
)
def test_get_pages(client, path, expect):
    rv = client.get(path, follow_redirects=True)
    assert rv.status_code == expect, f"{path} -> {rv.status_code}"


def test_text_redirect(client):
    rv = client.get("/text", follow_redirects=False)
    assert rv.status_code == 302
    assert "/legacy/text" in (rv.location or "")


def test_product_post_invalid_url(client):
    rv = client.post(
        "/product",
        data={"product_url": "not-a-url", "compare_url": ""},
        follow_redirects=True,
    )
    assert rv.status_code == 200
    assert b"valid product URL" in rv.data or b"http" in rv.data


def test_analyze_post_invalid_short_text(client):
    rv = client.post(
        "/analyze",
        data={"text": "short"},
        follow_redirects=True,
    )
    assert rv.status_code == 200
    assert b"characters" in rv.data or b"Please" in rv.data or b"emoji" in rv.data


def test_http_methods_not_allowed(client):
    """Routes that only define GET/POST should reject PUT with 405."""
    assert client.put("/").status_code == 405
    assert client.put("/product").status_code == 405
    assert client.put("/about").status_code == 405
    assert client.delete("/about").status_code == 405


def test_api_trends_json_shape(client):
    rv = client.get("/api/trends")
    assert rv.status_code == 200
    assert rv.is_json
    data = rv.get_json()
    assert "total_analyses" in data
    assert "avg_confidence" in data


def test_dashboard_stats_json_shape(client):
    rv = client.get("/api/dashboard-stats")
    assert rv.status_code == 200
    assert rv.is_json
    data = rv.get_json()
    assert "total_analyses" in data
    assert "emotion_distribution" in data


def test_logout_post_without_session(client):
    rv = client.post("/auth/logout", follow_redirects=False)
    # May redirect to login or home depending on implementation
    assert rv.status_code in (200, 302, 401)


def test_sklearn_analytics_rating_get(client):
    rv = client.get("/sklearn-analytics/rating", follow_redirects=True)
    assert rv.status_code == 200


@pytest.mark.skipif(
    os.environ.get("RUN_SLOW_TESTS") != "1",
    reason="Set RUN_SLOW_TESTS=1 to run analyze POST with full model + Mongo insert",
)
def test_analyze_post_valid_text_slow(client, mongo_reachable):
    if not mongo_reachable:
        pytest.skip("MongoDB not reachable")
    text = (
        "This is a valid sentence with enough words for the analyzer to accept "
        "the input and run emotion detection properly here."
    )
    rv = client.post("/analyze", data={"text": text}, follow_redirects=True)
    assert rv.status_code == 200
