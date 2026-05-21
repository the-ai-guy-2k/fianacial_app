import pytest
import os
import sys

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    import app as app_module
    test_app = app_module.app
    test_app.config['TESTING'] = True
    return test_app


@pytest.fixture
def client(app):
    """Create a Flask test client."""
    return app.test_client()
