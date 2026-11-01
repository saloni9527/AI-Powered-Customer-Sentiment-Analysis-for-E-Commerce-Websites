"""
Pytest config: ensure project root is on path before importing app (heavy: loads ML models once per session).
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def pytest_configure(config):
    os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-key-for-pytest")
    # Real MONGO_URI comes from .env when app loads; tests skip DB-heavy cases if ping fails.


@pytest.fixture(scope="session")
def flask_app():
    import app as app_module

    app_module.app.config["TESTING"] = True
    return app_module.app


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="session")
def mongo_reachable():
    try:
        import app as app_module

        app_module.client.admin.command("ping")
        return True
    except Exception:
        return False
