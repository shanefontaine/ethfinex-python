import requests


class PublicClient(object):
    """Ethfinex public client API."""

    def __init__(
        self,
        api_url: str = 'https://api.ethfinex.com/v2',
        timeout: int = 30
    ) -> None:
        """Create Ethfinex API public client."""
        self.url = api_url.rstrip('/')
        self.auth = None
        self.session = requests.Session()

    def get_platform_status(self) -> str:
        """Get the current status of the platform.
        Returns:
            1=operative
            0=maintenance
        """
        return self._send_message('/platform/status')

    def get_ticker(self, pair: str) -> list:
        """Get a list of available currency pairs for trading.
        Returns:
            [
                BID,
                BID_SIZE,
                ASK,
                ASK_SIZE,
                DAILY_CHANGE,
                DAILY_CHANGE_PERC,
                LAST_PRICE,
                VOLUME,
                HIGH,
                LOW
            ]
        """
        return self._send_message(f'/ticker/{pair}')

    def get_trades(
        self,
        pair: str,
        limit: int = None,
        start: int = None,
        end: int = None,
        sort: int = None
    ) -> list:
        """Get all the pertinent details of the trade, such as price, size and
        time. `sort=1` will sort results from old to new.
        Returns:
        [
            [
                ID,
                MTS,
                AMOUNT,
                PRICE
            ]
        ]
        """
        params = {}
        if limit:
            params['limit'] = limit
        if start and end and start < end:
            params['start'] = start
            params['end'] = end
        else:
            raise ValueError('The start time cannot be after the end time.')
        if sort:
            params['sort'] = sort
        return self._send_message(f'/trades/{pair}/hist', params=params)

    def get_books(
        self,
        pair: str,
        precision: str,
        len: int = None
    ) -> list:
        """Get the state of the Bitfinex order book. It is provided on a price
        aggregated basis, with customizable precision. Precision can be of the
        form P0, P1, P2, P3, P4, or R0. Len can be 25 or 100.
        Returns:
        [
            [
                PRICE,
                COUNT,
                AMOUNT
            ]
        ]
        """
        params = {}
        accepted_len = [25, 100]
        if len and len in accepted_len:
            params['len'] = len
            return self._send_message(f'/book/{pair}/{precision}', params=params)
        elif len and len not in accepted_len:
            raise ValueError('The len can only be 25 or 100.')

        return self._send_message(f'/book/{pair}/{precision}')

    def _send_message(
        self,
        endpoint: str,
        params: dict = None,
        data: str = None
    ) -> dict:
        """Send API request."""
        url = self.url + endpoint
        r = self.session.request('get', url, params=params, data=data,
                                 auth=self.auth, timeout=30)
        return r.json()
