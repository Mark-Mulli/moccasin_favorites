import boa
from eth_utils import to_wei

def test_price_feed_is_correct(coffee, price_feed):
    assert coffee.PRICE_FEED() == price_feed.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You need to spend more ETH!"):
        coffee.fund()