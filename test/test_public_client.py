import pytest
import time

from ethfinex.public_client import PublicClient


@pytest.fixture(scope='module')
def client():
    return PublicClient()


@pytest.mark.usefixtures('client')
class TestPublicClient(object):

    @staticmethod
    def teardown_method():
        time.sleep(.5)  # Avoid rate limit

    def test_get_platform_status(self, client):
        r = client.get_platform_status()
        assert type(r) is list

    @pytest.mark.parametrize('pair', ['tBTCUSD', 'tETHBTC'])
    def test_get_ticker(self, client, pair):
        r = client.get_ticker(pair)
        assert type(r) is list
        assert len(r) is 10

    @pytest.mark.parametrize('pair, limit, start, end, sort', [
        ('tBTCUSD', 120, None, None, 0),
        ('tBTCUSD', 120, 1514764800000, 1514765700000, 0),
        ('tBTCUSD', None, None, None, None),
        ('tBTCUSD', 10, 1514764800000, 1514765700000, 0),
        ('tBTCUSD', 10, 1514764800000, 1514768400000, 0),
        ('tBTCUSD', 10, 1514764800000, 1514768400000, 1),
        pytest.param('tBTCUSD', 10, 1514765700000, 1514764800000, 1,
                     marks=pytest.mark.xfail)
        ])
    def test_get_trades(self, client, pair, limit, start, end, sort):
        r = client.get_trades(pair, limit, start, end, sort)
        limit = 120 if not limit else limit

        # Check length
        assert len(r) == limit

        # Check timestamps
        if start and end:
            for entry in r:
                timestamp = entry[1]
                assert start <= timestamp <= end

        # Check sort
        if sort == 1:
            assert r[0][1] <= r[1][1]
        else:
            assert r[0][1] >= r[1][1]


        # if level is 1:
        #     ass
        #     pytest.fail('Fail: Level 1 should only return the best ask and bid')
        #
        # if level is 2 and (len(r['asks']) > 50 or len(r['bids']) > 50):
        #     pytest.fail('Fail: Level 2 should only return the top 50 asks and bids')
        #
        # if level is 3 and (len(r['asks']) < 50 or len(r['bids']) < 50):
        #     pytest.fail('Fail: Level 3 should return the full order book')
    # def test_get_product_ticker(self, client):
    #     r = client.get_product_ticker('BTC-USD')
    #     assert type(r) is dict
    #     assert 'ask' in r
    #     assert 'trade_id' in r
    #
    # def test_get_product_trades(self, client):
    #     r = list(islice(client.get_product_trades('BTC-USD'), 200))
    #     assert type(r) is list
    #     assert 'trade_id' in r[0]
    #
    # current_time = datetime.datetime.now()
    #
    # @pytest.mark.parametrize('start,end,granularity',
    #                          [(current_time - relativedelta(months=1),
    #                            current_time, 21600)])
    # def test_get_historic_rates(self, client, start, end, granularity):
    #     r = client.get_product_historic_rates('BTC-USD', start=start, end=end, granularity=granularity)
    #     assert type(r) is list
    #     for ticker in r:
    #         assert( all( [type(x) in (int, float) for x in ticker ] ) )
    #
    # def test_get_product_24hr_stats(self, client):
    #     r = client.get_product_24hr_stats('BTC-USD')
    #     assert type(r) is dict
    #     assert 'volume_30day' in r
    #
    # def test_get_currencies(self, client):
    #     r = client.get_currencies()
    #     assert type(r) is list
    #     assert 'name' in r[0]
    #
    # def test_get_time(self, client):
    #     r = client.get_time()
    #     assert type(r) is dict
    #     assert 'iso' in r