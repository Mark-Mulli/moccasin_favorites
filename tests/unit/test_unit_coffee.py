import boa
from eth_utils import to_wei

SEND_VALUE = to_wei(1, "ether")

def test_price_feed_is_correct(coffee, price_feed):
    assert coffee.PRICE_FEED() == price_feed.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You need to spend more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee, account):
    boa.env.set_balance(account.address, SEND_VALUE)
    coffee.fund(value = SEND_VALUE)
    funder = coffee.funders(0)
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE