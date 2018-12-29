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
            digits = len(price.split("."))
            # Will return either a whole number or a single decimal
            assert (digits == 1 or digits == 2)
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

    @pytest.mark.parametrize('symbol, key, side, section, sort', [
        ('fUSD', 'funding.size', 'long', 'hist', 0),
        ('fUSD', 'credits.size', 'long', 'hist', 0),
        # TODO: Figure out credits.size.sym
        # TODO: Figure out pos.size
        ('fUSD', 'funding.size', 'long', 'last', 0),
        ('fUSD', 'funding.size', 'long', 'last', 1),
        ('fUSD', 'credits.size', 'long', 'last', 1),
        pytest.param(None, None, None, None, None,
                     marks=pytest.mark.xfail)
        ])
    def test_get_stats(self, client, symbol, key, side, section, sort):
        r = client.get_stats(symbol, key, side, section, sort)

        # Check length
        if section == 'hist':
            assert len(r) == 120
        elif section == 'last':
            assert len(r) == 2

        # Check sort. There is no `section == 'last'` because you cannot sort
        # a single entry
        if sort == 1 and section == 'hist':
            assert r[0][0] <= r[1][0]
        elif sort != 1 and section == 'hist':
            assert r[0][0] >= r[1][0]

    @pytest.mark.parametrize('symbol, time_frame, section, limit, start, end, sort', [
        ('tBTCUSD', '1m', 'hist', None, None, None, None),
        ('tBTCUSD', '15m', 'hist', 1, None, None, None),
        ('tBTCUSD', '15m', 'hist', 1, None, None, 1),
        ('tBTCUSD', '15m', 'hist', 1, 1514764800000, 1514765700000, 1),
        ('tBTCUSD', '15m', 'hist', 1, 1514764800000, 1514768400000, 1),
        ('tBTCUSD', '1m', 'last', None, None, None, None),
        ('tBTCUSD', '15m', 'last', 1, 1514764800000, 1514768400000, 1),
        ('tBTCUSD', '1m', 'last', 1, 1514768400000, 1514764800000, 1),
        pytest.param(None, None, None, None, None, None, None,
                     marks=pytest.mark.xfail),
        pytest.param('tBTCUSD', '1m', 'hist', 1, 1514768400000, 1514764800000, 1,
                     marks=pytest.mark.xfail)
        ])
    def test_get_candles(self, client, symbol, time_frame, section, limit,
                         start, end, sort):
        r = client.get_candles(symbol, time_frame, section, limit,
                               start, end, sort)
        # Check length
        if section == 'hist' and limit != 1:
            assert len(r) == 120
        elif section == 'hist' and limit == 1:
            assert len(r) == 1
        elif section == 'last' and limit == 1:
            assert len(r) == 6
        elif section == 'last' and limit == 1:
            assert len(r) == 1

        # Check sort. There is no `section == 'last'` because you cannot sort
        # a single entry
        if sort == 1 and section == 'hist' and limit != 1:
            assert r[0][0] <= r[1][0]
        elif sort != 1 and section == 'hist' and limit != 1:
            assert r[0][0] >= r[1][0]
