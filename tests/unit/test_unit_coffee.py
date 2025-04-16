import boa
from eth_utils import to_wei
from tests.conftest import SEND_VALUE


RANDOM_USER = boa.env.generate_address("non_owner")

def test_price_feed_is_correct(coffee, price_feed):
    assert coffee.PRICE_FEED() == price_feed.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You need to spend more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee_funded):
    funder = coffee_funded.funders(0)
    assert coffee_funded.funder_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded):
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0

def test_multiple_funders_withdrawal(coffee, account):
    # Setup - Create 10 different funders with different amounts
    funders = [boa.env.generate_address(f"funder_{i}") for i in range(10)]
    amounts = [to_wei(i + 1, "ether") for i in range(10)]
    total_funded = sum(amounts)
    
    # Fund the contract with 10 different funders
    for i, funder in enumerate(funders):
        boa.env.set_balance(funder, amounts[i])
        with boa.env.prank(funder):
            coffee.fund(value=amounts[i])
    
    # Record owner's balance before withdrawal
    owner_balance_before = boa.env.get_balance(account.address)
    
    # Verify contract balance matches total funded
    assert boa.env.get_balance(coffee.address) == total_funded
    
    # Owner withdraws all funds
    with boa.env.prank(account.address):
        coffee.withdraw()
    
    # Assert contract balance is now 0
    assert boa.env.get_balance(coffee.address) == 0
    
    # Assert owner received all the funds
    owner_balance_after = boa.env.get_balance(account.address)
    assert owner_balance_after == owner_balance_before + total_funded
    
    # Verify funders array is empty after withdrawal
    with boa.reverts():  # Should revert when trying to access index 0 of empty array
        coffee.funders(0)
    
    # Check that all funder balances are reset to 0
    for funder in funders:
        assert coffee.funder_to_amount_funded(funder) == 0

def test_get_eth_to_usd(coffee):
    assert coffee.get_eth_to_usd(SEND_VALUE) > 0