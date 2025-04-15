import pytest
from script.deploy import deploy_coffee
from script.deploy_mocks import deploy_feed
from moccasin.config import get_active_network

@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account()

@pytest.fixture(scope="session")
def price_feed():
    return deploy_feed()


@pytest.fixture(scope="function")
def coffee(price_feed):
    return deploy_coffee(price_feed)