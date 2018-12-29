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

    @pytest.mark.skip
    def test_get_platform_status(self, client):
        r = client.get_platform_status()
        assert type(r) is list

    @pytest.mark.skip
    @pytest.mark.parametrize('pair', ['tBTCUSD', 'tETHBTC'])
    def test_get_ticker(self, client, pair):
        r = client.get_ticker(pair)
        assert type(r) is list
        assert len(r) is 10

    @pytest.mark.skip
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

    @pytest.mark.parametrize('pair, precision, length', [
        ('tBTCUSD', 'P0', None),
        ('tBTCUSD', 'P0', 25),
        ('tBTCUSD', 'P0', 100),
        ('tBTCUSD', 'P4', None),
        ('tBTCUSD', 'P1', 25),
        ('tBTCUSD', 'P2', 25),
        pytest.param('tBTCUSD', 'P2', 5,
                     marks=pytest.mark.xfail),
        pytest.param('tBTCUSD', None, 5,
                     marks=pytest.mark.xfail),
        ])
    def test_get_books(self, client, pair, precision, length):
        r = client.get_books(pair, precision, length)

        # Default length is 50. Returns double the amount
        length = 50 if not length else length * 2

        # Check length
        assert len(r) == length

        # Check Precision
        price = str(r[0][0])
        if precision == 'P0':
            digits = len(price.split(".")[1])
            assert digits == 1
        elif precision == 'P1':
            assert len(price) == 4
        elif precision == 'P2':
            assert len(price) == 4
            assert price[-1] == '0'
        elif precision == 'P3':
            assert len(price) == 4
            assert price[-1] == '0'
            assert price[-2] == '0'
        elif precision == 'P4':
            assert len(price) == 4
            assert price[-1] == '0'
            assert price[-2] == '0'
            assert price[-3] == '0'
        elif precision == 'R0':
            assert len(price == 11)
