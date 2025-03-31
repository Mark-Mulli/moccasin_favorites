from interfaces import AggregatorV3Interface

PRECISION: constant(uint256) = (1 * (10 ** 18))
   
@internal
@view
def _get_eth_to_usd(price_feed: AggregatorV3Interface, eth_amount: uint256) -> uint256:

    price: int256 = staticcall price_feed.latestAnswer() # 271683000000

    eth_price: uint256 = convert(price, uint256) * (10 ** 10)

    eth_amount_in_usd: uint256 = (eth_amount*eth_price) // PRECISION

    return eth_amount_in_usd
