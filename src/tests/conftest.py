import os

import pytest
from starlette.testclient import TestClient

from app.config import Settings, get_settings
from app.main import create_api


def get_settings_override():
    return Settings(testing=True, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # setup
    api = create_api()
    api.dependency_overrides[get_settings] = get_settings_override
    with TestClient(api) as test_client:

        # testing
        yield test_client

    # tear down
