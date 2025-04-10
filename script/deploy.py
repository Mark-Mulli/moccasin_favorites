from src import buy_me_a_coffee
from moccasin.config import get_active_network
# from script.deploy_mocks import deploy_feed
from moccasin.boa_tools import VyperContract    

def deploy_coffee(price_feed: str) -> VyperContract:
    coffee_contract: VyperContract = buy_me_a_coffee.deploy(price_feed)
    active_network = get_active_network()
    
    if active_network.has_explorer():
        result  = active_network.moccasin_verify(coffee_contract)
        result.wait_for_verification()    
    return coffee_contract

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    # price_feed: VyperContract = deploy_feed()
    # coffee: VyperContract = deploy_coffee(price_feed)
    # print("Coffee deployed at", coffee.address)
    
    #using manifest named
    price_feed = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name} using price feed at {price_feed.address}")
    return deploy_coffee(price_feed)