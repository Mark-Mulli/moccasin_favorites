from src.mock import mock_V3_aggregator
from moccasin.boa_tools import VyperContract

STATRING_DECIMAL = 8
STARTING_PRICE = int(2000e8)

def deploy_feed() -> VyperContract:
    return mock_V3_aggregator.deploy(
        STATRING_DECIMAL, STARTING_PRICE
    )

def moccasin_main() -> VyperContract:
    return deploy_feed()